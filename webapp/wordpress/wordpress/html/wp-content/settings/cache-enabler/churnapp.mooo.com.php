<?php
/**
 * The settings file for Cache Enabler.
 *
 * This file is automatically created, mirroring the plugin settings saved in the
 * database. It is used to cache and deliver pages.
 *
 * @site  http://churnapp.mooo.com
 * @time  Sat, 19 Apr 2025 12:54:01 GMT
 *
 * @since  1.5.0
 * @since  1.6.0  The `clear_site_cache_on_saved_post` setting was added.
 * @since  1.6.0  The `clear_complete_cache_on_saved_post` setting was removed.
 * @since  1.6.0  The `clear_site_cache_on_new_comment` setting was added.
 * @since  1.6.0  The `clear_complete_cache_on_new_comment` setting was removed.
 * @since  1.6.0  The `clear_site_cache_on_changed_plugin` setting was added.
 * @since  1.6.0  The `clear_complete_cache_on_changed_plugin` setting was removed.
 * @since  1.6.1  The `clear_site_cache_on_saved_comment` setting was added.
 * @since  1.6.1  The `clear_site_cache_on_new_comment` setting was removed.
 * @since  1.7.0  The `mobile_cache` setting was added.
 * @since  1.8.0  The `use_trailing_slashes` setting was added.
 * @since  1.8.0  The `permalink_structure` setting was deprecated.
 */

return array (
  'version' => '1.8.15',
  'use_trailing_slashes' => 1,
  'permalink_structure' => 'has_trailing_slash',
  'cache_expires' => 1,
  'cache_expiry_time' => 8,
  'clear_site_cache_on_saved_post' => 0,
  'clear_site_cache_on_saved_comment' => 0,
  'clear_site_cache_on_saved_term' => 0,
  'clear_site_cache_on_saved_user' => 0,
  'clear_site_cache_on_changed_plugin' => 0,
  'convert_image_urls_to_webp' => 0,
  'mobile_cache' => 0,
  'compress_cache' => 1,
  'minify_html' => 1,
  'minify_inline_css_js' => 1,
  'excluded_post_ids' => '',
  'excluded_page_paths' => '',
  'excluded_query_strings' => '',
  'excluded_cookies' => '',
);