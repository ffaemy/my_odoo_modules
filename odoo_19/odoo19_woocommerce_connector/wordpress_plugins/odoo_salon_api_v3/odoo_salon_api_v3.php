<?php
/**
 * Plugin Name: Odoo Salon Booking API V3
 * Description: Minimal Salon Booking System helper endpoint for Odoo tutorial imports.
 * Version: 1.0.0
 * Author: Odooistic
 */

if (!defined('ABSPATH')) {
    exit;
}

define('ODOO_SALON_API_V3_OPTION', 'odoo_salon_api_v3_token');

function odoo_salon_api_v3_activate()
{
    if (!get_option(ODOO_SALON_API_V3_OPTION)) {
        update_option(ODOO_SALON_API_V3_OPTION, wp_generate_password(32, false, false));
    }
}
register_activation_hook(__FILE__, 'odoo_salon_api_v3_activate');

function odoo_salon_api_v3_admin_menu()
{
    add_options_page(
        'Odoo Salon API V3',
        'Odoo Salon API V3',
        'manage_options',
        'odoo-salon-api-v3',
        'odoo_salon_api_v3_settings_page'
    );
}
add_action('admin_menu', 'odoo_salon_api_v3_admin_menu');

function odoo_salon_api_v3_settings_page()
{
    if (!current_user_can('manage_options')) {
        return;
    }

    if (isset($_POST['odoo_salon_api_v3_save'])) {
        check_admin_referer('odoo_salon_api_v3_save');
        $token = isset($_POST['odoo_salon_api_v3_token']) ? sanitize_text_field(wp_unslash($_POST['odoo_salon_api_v3_token'])) : '';
        update_option(ODOO_SALON_API_V3_OPTION, $token ? $token : wp_generate_password(32, false, false));
        echo '<div class="updated"><p>Odoo Salon API V3 token saved.</p></div>';
    }

    $token = esc_attr(get_option(ODOO_SALON_API_V3_OPTION));
    ?>
    <div class="wrap">
        <h1>Odoo Salon API V3</h1>
        <p><strong>Health endpoint:</strong> <code><?php echo esc_url(rest_url('odoo-salon/v3/health')); ?></code></p>
        <p><strong>Bookings endpoint:</strong> <code><?php echo esc_url(rest_url('odoo-salon/v3/bookings')); ?></code></p>
        <form method="post">
            <?php wp_nonce_field('odoo_salon_api_v3_save'); ?>
            <table class="form-table">
                <tr>
                    <th scope="row"><label for="odoo_salon_api_v3_token">API Token</label></th>
                    <td>
                        <input id="odoo_salon_api_v3_token" name="odoo_salon_api_v3_token" type="text" class="regular-text" value="<?php echo $token; ?>">
                    </td>
                </tr>
            </table>
            <?php submit_button('Save Token', 'primary', 'odoo_salon_api_v3_save'); ?>
        </form>
    </div>
    <?php
}

function odoo_salon_api_v3_register_routes()
{
    register_rest_route('odoo-salon/v3', '/health', array(
        'methods' => 'GET',
        'callback' => 'odoo_salon_api_v3_health',
        'permission_callback' => 'odoo_salon_api_v3_check_token',
    ));
    register_rest_route('odoo-salon/v3', '/bookings', array(
        'methods' => 'GET',
        'callback' => 'odoo_salon_api_v3_bookings',
        'permission_callback' => 'odoo_salon_api_v3_check_token',
    ));
}
add_action('rest_api_init', 'odoo_salon_api_v3_register_routes');

function odoo_salon_api_v3_check_token($request)
{
    $configured = (string) get_option(ODOO_SALON_API_V3_OPTION);
    $provided = (string) $request->get_param('token');
    $header = (string) $request->get_header('x-odoo-salon-token');
    if ($header) {
        $provided = $header;
    }
    return $configured && $provided && $configured === $provided;
}

function odoo_salon_api_v3_health($request)
{
    return array(
        'ok' => true,
        'site' => get_bloginfo('name'),
        'time' => current_time('mysql'),
    );
}

function odoo_salon_api_v3_bookings($request)
{
    $limit = max(1, min(50, absint($request->get_param('per_page') ? $request->get_param('per_page') : 20)));
    $booking_id = absint($request->get_param('booking_id') ? $request->get_param('booking_id') : 0);
    $post_types = array('sln_booking', 'sln_reservation');

    $args = array(
        'post_type' => $post_types,
        'post_status' => 'any',
        'posts_per_page' => $limit,
        'orderby' => 'ID',
        'order' => 'DESC',
        'no_found_rows' => true,
    );
    if ($booking_id) {
        $args['p'] = $booking_id;
        unset($args['posts_per_page']);
    }

    $query = new WP_Query($args);
    $bookings = array();

    foreach ($query->posts as $post) {
        $meta = get_post_meta($post->ID);
        $meta_keys = array_keys($meta);
        $plain = odoo_salon_api_v3_plain_meta($meta);

        $date = odoo_salon_api_v3_value($plain, array('date', 'day'));
        $time = odoo_salon_api_v3_value($plain, array('time', 'hour'));
        $start = odoo_salon_api_v3_value($plain, array('start', 'from', 'datetime'));
        if (!$start && $date && $time) {
            $start = trim($date . ' ' . $time);
        }

        $bookings[] = array(
            'id' => (int) $post->ID,
            'post_type' => $post->post_type,
            'status' => $post->post_status,
            'service' => odoo_salon_api_v3_value($plain, array('service', 'services')) ?: $post->post_title,
            'staff' => odoo_salon_api_v3_value($plain, array('attendant', 'assistant', 'staff')),
            'start' => $start,
            'stop' => odoo_salon_api_v3_value($plain, array('end', 'to', 'stop')),
            'duration_hours' => 1,
            'price' => odoo_salon_api_v3_value($plain, array('price', 'amount', 'total')),
            'notes' => odoo_salon_api_v3_value($plain, array('note', 'message', 'comment')),
            'customer' => array(
                'name' => odoo_salon_api_v3_value($plain, array('fullname', 'customername', 'name')),
                'first_name' => odoo_salon_api_v3_value($plain, array('firstname')),
                'last_name' => odoo_salon_api_v3_value($plain, array('lastname')),
                'email' => odoo_salon_api_v3_value($plain, array('email', 'mail')),
                'phone' => odoo_salon_api_v3_value($plain, array('phone', 'mobile', 'tel')),
            ),
            'raw_meta_keys' => $meta_keys,
        );
    }

    return array(
        'count' => count($bookings),
        'bookings' => $bookings,
    );
}

function odoo_salon_api_v3_plain_meta($meta)
{
    $result = array();
    foreach ((array) $meta as $key => $values) {
        $value = is_array($values) && isset($values[0]) ? $values[0] : '';
        if (is_scalar($value)) {
            $result[(string) $key] = (string) $value;
        }
    }
    return $result;
}

function odoo_salon_api_v3_value($plain, $needles)
{
    foreach ((array) $plain as $key => $value) {
        $normalized = preg_replace('/[^a-z0-9]+/', '', strtolower((string) $key));
        foreach ($needles as $needle) {
            $needle = preg_replace('/[^a-z0-9]+/', '', strtolower((string) $needle));
            if ($value !== '' && strpos($normalized, $needle) !== false) {
                return $value;
            }
        }
    }
    return '';
}
