<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /** @var array<string, list<string>> */
    private const RETIRED_VALUES = [
        'banner_path' => ['images/Bannernew.jpg'],
        'opac_banner_path' => ['images/Bannernew.jpg'],
        'opac_logo_path' => ['img/usm_logo_1954.png'],
        'sidebar_logo_path' => ['img/usm_logo_1954.png'],
        'login_modal_logo_path' => ['img/usm_logo_1954.png'],
        'register_modal_attendance_logo_path' => ['img/usm_logo_1954.png'],
        'register_modal_library_logo_path' => ['img/usm_logo_1954.png'],
        'sidebar_brand_name' => ['USM Library'],
        'sidebar_brand_subtitle' => ['KEPLRC Portal'],
        'login_modal_portal_name' => ['USM Library Portal'],
        'login_modal_description' => ['Sign in to access the University of Southern Mindanao Library system.'],
        'login_modal_email_placeholder' => ['staff@usm.edu.ph'],
        'register_modal_attendance_portal_name' => ['USM Attendance'],
        'register_modal_library_portal_name' => ['USM Library'],
        'primary_color' => ['#1B5E20', '#1b5e20'],
        'secondary_color' => ['#2E7D32', '#2e7d32'],
        'accent_color' => ['#FFD700', '#ffd700'],
        'sidebar_active_color' => ['#1B5E20', '#1b5e20'],
        'button_color' => ['#1B5E20', '#1b5e20'],
        'table_hover_color' => ['#E8F5E9', '#e8f5e9'],
        'login_modal_left_background_color' => ['#1B5E20', '#1b5e20'],
        'login_modal_description_color' => ['#DCFCE7', '#dcfce7'],
        'login_modal_button_color' => ['#1B5E20', '#1b5e20'],
        'register_modal_attendance_panel_color' => ['#2E7D32', '#2e7d32'],
        'register_modal_attendance_accent_color' => ['#FFD700', '#ffd700'],
        'register_modal_attendance_active_role_color' => ['#2E7D32', '#2e7d32'],
        'register_modal_attendance_submit_color' => ['#2E7D32', '#2e7d32'],
        'register_modal_library_panel_color' => ['#1B5E20', '#1b5e20'],
        'register_modal_library_accent_color' => ['#1B5E20', '#1b5e20'],
        'register_modal_library_active_role_color' => ['#2E7D32', '#2e7d32'],
        'register_modal_library_submit_color' => ['#1B5E20', '#1b5e20'],
    ];

    public function up(): void
    {
        if (! Schema::hasTable('branding_settings')) {
            return;
        }

        foreach (self::RETIRED_VALUES as $column => $values) {
            if (! Schema::hasColumn('branding_settings', $column)) {
                continue;
            }

            DB::table('branding_settings')
                ->whereIn($column, $values)
                ->update([$column => null]);
        }

        Cache::forget('branding.active');
    }

    public function down(): void
    {
        // Retired USM defaults were cleared so the PBCC defaults in config apply.
    }
};
