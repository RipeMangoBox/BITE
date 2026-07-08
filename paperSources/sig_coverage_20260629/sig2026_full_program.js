jQuery(function() {

    if (typeof is_agenda_page != 'undefined' && is_agenda_page) {
        // We don't want to respect the persistant date / filters on this page.
        // date_sel is a global that we don't want to set.
        return;
    }

    full_program_show_filters();

    // date_sel = jQuery('[name=date_sel]');
    // show_date(date_sel.val());
    // full_program_filter_on_selectors();
    // show_hide_empty_msg();

    date_sel = jQuery('[name=date_sel]');
    let date_ = date_sel.val();

    try {
        date_ = JSON.parse(window.sessionStorage['date_sel']);
    } catch (error) {
        date_ = date_sel.val();
    }

    show_date(date_);

	full_program_page_setup();
    // full_program_fill_filters_from_query();
    var used_query = full_program_fill_filters_from_query();
    if (!used_query) {
        load_filter_opts();
        update_filter_display();
    }

    jQuery('.small-date-sels').on('click', show_hide_empty_msg);
    jQuery('.large-date-sel').on('click', show_hide_empty_msg);

    // jQuery('[name=etype_filt]').on('change', full_program_filter_event_handler);
    // jQuery('[name^="ptrack_filt"]').on('change', full_program_filter_event_handler);

    // jQuery('[name=etype_filt]').on('change', save_filter_opts);
    // jQuery('[name^="ptrack_filt"]').on('change', save_filter_opts);

    jQuery('[name=etype_filt]').on('change', filter_change_actions);
    jQuery('[name=room_filt]').on('change', filter_change_actions);
    jQuery('[name=time_filt]').on('change', filter_change_actions);
    jQuery('[name^="ptrack_filt"]').on('change', filter_change_actions);
    jQuery('[name="date_sel"]').on('change', filter_change_actions);

    // jQuery(window).on('scroll resize', show_hide_filter_display);
    jQuery(document).on('click', '.current_filter_val', handle_remove_event)

    // This helps select2 filters show the default text.
    // This is too broad - specifically we don't want to trigger the timezone select
    // change event as that reloads the page.
    // jQuery('select').trigger('change');

    // Here is a more specific way to do it.  Are there more?
    jQuery('[name=etype_filt]').trigger('change');
    jQuery('[name=room_filt]').trigger('change');
    jQuery('[name^="ptrack_filt"]').trigger('change');
    jQuery('[name=time_filt]').trigger('change');
})

function filter_change_actions() {
    // We don't want to do this on other pages.
    // Maybe just not on the agenda page?
    // Could change to is_agenda_page()
    if (!is_full_program_page()) {
        return;
    }
    full_program_filter_event_handler();
    save_filter_opts();
    update_filter_display();
}