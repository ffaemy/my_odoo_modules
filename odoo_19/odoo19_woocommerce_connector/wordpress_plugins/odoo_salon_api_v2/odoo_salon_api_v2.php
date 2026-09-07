<?php
/**
 * Plugin Name: Odoo Salon Booking API V2
 * Description: Collision-safe helper endpoint for importing Salon Booking System reservations into Odoo.
 * Version: 1.0.0
 * Author: Odooistic
 */

if (!defined('ABSPATH')) {
    exit;
}

define('ODOO_SALON_API_V2_OPTION', 'odoo_salon_api_v2_token');

register_activation_hook(__FILE__, 'odoo_salon_api_v2_activate');
function odoo_salon_api_v2_activate()
{
    if (!get_option(ODOO_SALON_API_V2_OPTION)) {
        update_option(ODOO_SALON_API_V2_OPTION, wp_generate_password(32, false, false));
    }
}

add_action('admin_menu', 'odoo_salon_api_v2_admin_menu');
function odoo_salon_api_v2_admin_menu()
{
    add_options_page(
        'Odoo Salon API V2',
        'Odoo Salon API V2',
        'manage_options',
        'odoo-salon-api-v2',
        'odoo_salon_api_v2_settings_page'
    );
}

function odoo_salon_api_v2_settings_page()
{
    if (!current_user_can('manage_options')) {
        return;
    }

    if (isset($_POST['odoo_salon_api_v2_save'])) {
        check_admin_referer('odoo_salon_api_v2_save');
        $token = sanitize_text_field(wp_unslash(isset($_POST['odoo_salon_api_v2_token']) ? $_POST['odoo_salon_api_v2_token'] : ''));
        update_option(ODOO_SALON_API_V2_OPTION, $token ? $token : wp_generate_password(32, false, false));
        echo '<div class="updated"><p>Odoo Salon API V2 token saved.</p></div>';
    }

    $token = esc_attr(get_option(ODOO_SALON_API_V2_OPTION));
    $endpoint = esc_url(rest_url('odoo-salon/v2/bookings'));
    ?>
    <div class="wrap">
        <h1>Odoo Salon API V2</h1>
        <p>Use this endpoint in Odoo to import Salon Booking System reservations.</p>
        <p><strong>Endpoint:</strong> <code><?php echo $endpoint; ?></code></p>
        <form method="post">
            <?php wp_nonce_field('odoo_salon_api_v2_save'); ?>
            <table class="form-table">
                <tr>
                    <th scope="row"><label for="odoo_salon_api_v2_token">API Token</label></th>
                    <td>
                        <input id="odoo_salon_api_v2_token" name="odoo_salon_api_v2_token" type="text" class="regular-text" value="<?php echo $token; ?>">
                    </td>
                </tr>
            </table>
            <?php submit_button('Save Token', 'primary', 'odoo_salon_api_v2_save'); ?>
        </form>
    </div>
    <?php
}

add_action('rest_api_init', 'odoo_salon_api_v2_register_routes');
function odoo_salon_api_v2_register_routes()
{
    register_rest_route('odoo-salon/v2', '/bookings', array(
        'methods' => 'GET',
        'callback' => 'odoo_salon_api_v2_get_bookings',
        'permission_callback' => 'odoo_salon_api_v2_check_token',
    ));
}

function odoo_salon_api_v2_check_token($request)
{
    $configured = (string) get_option(ODOO_SALON_API_V2_OPTION);
    $provided = (string) ($request->get_header('x-odoo-salon-token') ? $request->get_header('x-odoo-salon-token') : $request->get_param('token'));
    return $configured && $provided && hash_equals($configured, $provided);
}

function odoo_salon_api_v2_get_bookings($request)
{
    global $wpdb;

    $limit = max(1, min(100, absint($request->get_param('per_page') ? $request->get_param('per_page') : 20)));
    $booking_id = absint($request->get_param('booking_id') ? $request->get_param('booking_id') : 0);

    if ($booking_id) {
        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT ID, post_type, post_status, post_title, post_date FROM {$wpdb->posts} WHERE ID = %d LIMIT 1",
            $booking_id
        ));
    } else {
        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT ID, post_type, post_status, post_title, post_date
             FROM {$wpdb->posts}
             WHERE post_type = %s AND post_status NOT IN ('auto-draft', 'trash')
             ORDER BY ID DESC LIMIT %d",
            'sln_booking',
            $limit
        ));
    }

    $bookings = array();
    foreach ((array) $rows as $row) {
        $meta = odoo_salon_api_v2_normalize_meta(get_post_meta($row->ID));
        $flat = odoo_salon_api_v2_flatten($meta);
        $date = odoo_salon_api_v2_find_value($flat, array('date', 'day', 'bookingdate'));
        $time = odoo_salon_api_v2_find_value($flat, array('time', 'hour', 'starttime'));
        $start = odoo_salon_api_v2_find_value($flat, array('start', 'from', 'datetime'));
        if (!$start && $date && $time) {
            $start = trim($date . ' ' . $time);
        }

        $bookings[] = array(
            'id' => (int) $row->ID,
            'post_type' => $row->post_type,
            'status' => $row->post_status,
            'service' => odoo_salon_api_v2_find_value($flat, array('service', 'services')) ? odoo_salon_api_v2_find_value($flat, array('service', 'services')) : $row->post_title,
            'staff' => odoo_salon_api_v2_find_value($flat, array('attendant', 'assistant', 'staff')),
            'start' => $start,
            'stop' => odoo_salon_api_v2_find_value($flat, array('end', 'to', 'stop')),
            'duration_hours' => odoo_salon_api_v2_duration_to_hours(odoo_salon_api_v2_find_value($flat, array('duration'))),
            'price' => odoo_salon_api_v2_find_value($flat, array('price', 'amount', 'total')),
            'notes' => odoo_salon_api_v2_find_value($flat, array('note', 'message', 'comment')),
            'customer' => array(
                'name' => odoo_salon_api_v2_find_value($flat, array('fullname', 'customername', 'name')),
                'first_name' => odoo_salon_api_v2_find_value($flat, array('firstname', 'first_name')),
                'last_name' => odoo_salon_api_v2_find_value($flat, array('lastname', 'last_name')),
                'email' => odoo_salon_api_v2_find_value($flat, array('email', 'mail')),
                'phone' => odoo_salon_api_v2_find_value($flat, array('phone', 'mobile', 'tel')),
            ),
            'raw_meta_keys' => array_keys($meta),
        );
    }

    return rest_ensure_response(array(
        'count' => count($bookings),
        'bookings' => $bookings,
    ));
}

function odoo_salon_api_v2_normalize_meta($meta)
{
    $result = array();
    foreach ((array) $meta as $key => $values) {
        $value = is_array($values) && count($values) === 1 ? $values[0] : $values;
        $result[$key] = is_string($value) ? maybe_unserialize($value) : $value;
    }
    return $result;
}

function odoo_salon_api_v2_flatten($value, $prefix = '', $depth = 0)
{
    if ($depth > 4) {
        return array();
    }
    $flat = array();
    if (is_array($value)) {
        foreach ($value as $key => $child) {
            $child_key = $prefix ? $prefix . '.' . $key : (string) $key;
            $flat = array_merge($flat, odoo_salon_api_v2_flatten($child, $child_key, $depth + 1));
        }
        return $flat;
    }
    if (is_object($value)) {
        return odoo_salon_api_v2_flatten((array) $value, $prefix, $depth + 1);
    }
    $flat[$prefix] = is_scalar($value) ? (string) $value : '';
    return $flat;
}

function odoo_salon_api_v2_find_value($flat, $needles)
{
    foreach ((array) $flat as $key => $value) {
        $normalized = preg_replace('/[^a-z0-9]+/', '', strtolower($key));
        foreach ($needles as $needle) {
            $needle = preg_replace('/[^a-z0-9]+/', '', strtolower($needle));
            if ($value !== '' && strpos($normalized, $needle) !== false) {
                return $value;
            }
        }
    }
    return '';
}

function odoo_salon_api_v2_duration_to_hours($duration)
{
    if (!$duration) {
        return 1;
    }
    if (is_numeric($duration)) {
        return ((float) $duration) > 10 ? ((float) $duration) / 60 : (float) $duration;
    }
    if (preg_match('/^(\d+):(\d+)/', $duration, $matches)) {
        return ((int) $matches[1]) + (((int) $matches[2]) / 60);
    }
    return 1;
}
