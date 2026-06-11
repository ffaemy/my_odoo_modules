<?php
/**
 * Plugin Name: Odoo Salon Booking API
 * Description: Exposes Salon Booking System reservations to Odoo for tutorial imports.
 * Version: 1.0.1
 * Author: Odooistic
 */

if (!defined('ABSPATH')) {
    exit;
}

define('ODOO_SALON_API_OPTION', 'odoo_salon_api_token');

register_activation_hook(__FILE__, function () {
    if (!get_option(ODOO_SALON_API_OPTION)) {
        update_option(ODOO_SALON_API_OPTION, wp_generate_password(32, false, false));
    }
});

add_action('admin_menu', function () {
    add_options_page(
        'Odoo Salon API',
        'Odoo Salon API',
        'manage_options',
        'odoo-salon-api',
        'odoo_salon_api_settings_page'
    );
});

function odoo_salon_api_settings_page()
{
    if (!current_user_can('manage_options')) {
        return;
    }

    if (isset($_POST['odoo_salon_api_save'])) {
        check_admin_referer('odoo_salon_api_save');
        $token = sanitize_text_field(wp_unslash($_POST['odoo_salon_api_token'] ?? ''));
        update_option(ODOO_SALON_API_OPTION, $token ?: wp_generate_password(32, false, false));
        echo '<div class="updated"><p>Odoo Salon API token saved.</p></div>';
    }

    $token = esc_attr(get_option(ODOO_SALON_API_OPTION));
    $endpoint = esc_url(rest_url('odoo-salon/v1/bookings'));
    ?>
    <div class="wrap">
        <h1>Odoo Salon API</h1>
        <p>Use this endpoint in Odoo to import Salon Booking System reservations.</p>
        <p><strong>Endpoint:</strong> <code><?php echo $endpoint; ?></code></p>
        <form method="post">
            <?php wp_nonce_field('odoo_salon_api_save'); ?>
            <table class="form-table">
                <tr>
                    <th scope="row"><label for="odoo_salon_api_token">API Token</label></th>
                    <td>
                        <input id="odoo_salon_api_token" name="odoo_salon_api_token" type="text" class="regular-text" value="<?php echo $token; ?>">
                    </td>
                </tr>
            </table>
            <?php submit_button('Save Token', 'primary', 'odoo_salon_api_save'); ?>
        </form>
    </div>
    <?php
}

add_action('rest_api_init', function () {
    register_rest_route('odoo-salon/v1', '/bookings', array(
        'methods' => 'GET',
        'callback' => 'odoo_salon_api_get_bookings',
        'permission_callback' => 'odoo_salon_api_check_token',
    ));
});

function odoo_salon_api_check_token(WP_REST_Request $request)
{
    $configured = (string) get_option(ODOO_SALON_API_OPTION);
    $provided = (string) ($request->get_header('x-odoo-salon-token') ?: $request->get_param('token'));
    return $configured && $provided && hash_equals($configured, $provided);
}

function odoo_salon_api_get_bookings(WP_REST_Request $request)
{
    try {
        return odoo_salon_api_get_bookings_safe($request);
    } catch (Throwable $exception) {
        return new WP_Error(
            'odoo_salon_api_error',
            $exception->getMessage(),
            array('status' => 500)
        );
    }
}

function odoo_salon_api_get_bookings_safe(WP_REST_Request $request)
{
    global $wpdb;

    $limit = max(1, min(100, absint($request->get_param('per_page') ?: 20)));
    $booking_id = absint($request->get_param('booking_id') ?: 0);

    if ($booking_id) {
        $rows = $wpdb->get_results(
            $wpdb->prepare(
                "SELECT ID, post_type, post_status, post_title, post_date
                 FROM {$wpdb->posts}
                 WHERE ID = %d
                 LIMIT 1",
                $booking_id
            )
        );
    } else {
        $rows = $wpdb->get_results(
            $wpdb->prepare(
                "SELECT ID, post_type, post_status, post_title, post_date
                 FROM {$wpdb->posts}
                 WHERE post_type = %s
                   AND post_status NOT IN ('auto-draft', 'trash')
                 ORDER BY ID DESC
                 LIMIT %d",
                'sln_booking',
                $limit
            )
        );

        if (!$rows) {
            $rows = $wpdb->get_results(
                $wpdb->prepare(
                    "SELECT ID, post_type, post_status, post_title, post_date
                     FROM {$wpdb->posts}
                     WHERE post_type LIKE %s
                       AND post_status NOT IN ('auto-draft', 'trash')
                     ORDER BY ID DESC
                     LIMIT %d",
                    $wpdb->esc_like('sln_') . '%',
                    $limit
                )
            );
        }
    }

    $bookings = array();
    foreach ($rows as $row) {
        $meta = odoo_salon_api_normalize_meta(get_post_meta($row->ID));
        $booking = odoo_salon_api_extract_booking($row, $meta);
        $bookings[] = $booking;
    }

    return rest_ensure_response(array(
        'count' => count($bookings),
        'bookings' => $bookings,
    ));
}

function odoo_salon_api_normalize_meta($meta)
{
    $result = array();
    foreach ($meta as $key => $values) {
        $value = count($values) === 1 ? $values[0] : $values;
        $result[$key] = is_string($value) ? maybe_unserialize($value) : $value;
    }
    return $result;
}

function odoo_salon_api_extract_booking($row, $meta)
{
    $flat = odoo_salon_api_flatten($meta);
    $date = odoo_salon_api_find_value($flat, array('date', 'day', 'booking_date'));
    $time = odoo_salon_api_find_value($flat, array('time', 'hour', 'start_time'));
    $start = odoo_salon_api_find_value($flat, array('start', 'from', 'datetime'));
    $stop = odoo_salon_api_find_value($flat, array('end', 'to', 'stop'));
    $duration = odoo_salon_api_find_value($flat, array('duration'));

    if (!$start && $date && $time) {
        $start = trim($date . ' ' . $time);
    }

    return array(
        'id' => (int) $row->ID,
        'post_type' => $row->post_type,
        'status' => $row->post_status,
        'service' => odoo_salon_api_find_value($flat, array('service', 'services')) ?: $row->post_title,
        'staff' => odoo_salon_api_find_value($flat, array('attendant', 'assistant', 'staff')),
        'start' => $start,
        'stop' => $stop,
        'duration_hours' => odoo_salon_api_duration_to_hours($duration),
        'price' => odoo_salon_api_find_value($flat, array('price', 'amount', 'total')),
        'notes' => odoo_salon_api_find_value($flat, array('note', 'message', 'comment')),
        'customer' => array(
            'name' => odoo_salon_api_find_value($flat, array('fullname', 'customer_name', 'name')),
            'first_name' => odoo_salon_api_find_value($flat, array('firstname', 'first_name')),
            'last_name' => odoo_salon_api_find_value($flat, array('lastname', 'last_name')),
            'email' => odoo_salon_api_find_value($flat, array('email', 'mail')),
            'phone' => odoo_salon_api_find_value($flat, array('phone', 'mobile', 'tel')),
        ),
        'raw_meta_keys' => array_keys($meta),
    );
}

function odoo_salon_api_flatten($value, $prefix = '', $depth = 0)
{
    if ($depth > 5) {
        return array();
    }
    $flat = array();
    if (is_array($value)) {
        foreach ($value as $key => $child) {
            $child_key = $prefix ? $prefix . '.' . $key : (string) $key;
            $flat = array_merge($flat, odoo_salon_api_flatten($child, $child_key, $depth + 1));
        }
        return $flat;
    }
    if (is_object($value)) {
        return odoo_salon_api_flatten((array) $value, $prefix, $depth + 1);
    }
    $flat[$prefix] = is_scalar($value) ? (string) $value : '';
    return $flat;
}

function odoo_salon_api_find_value($flat, $needles)
{
    foreach ($flat as $key => $value) {
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

function odoo_salon_api_duration_to_hours($duration)
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
