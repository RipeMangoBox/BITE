// var is_agenda_page;
// var is_happening_now_page;


(function( $ ) {
	'use strict';

	/**
	 * All of the code for your public-facing JavaScript source
	 * should reside in this file.
	 *
	 * Note: It has been assumed you will write jQuery code here, so the
	 * $ function reference has been prepared for usage within the scope
	 * of this function.
	 *
	 */

	$(function() {

		// This is to allow the maps page back button to work correctly.
		update_goback_url();

		// Handle wordpress login agenda sync auth.
		// The WP_LLVP_AGENDA_SYNC_USER var is set by PHP when a user is logged
		// in that should have their WP login used for agenda sync.
		let original_uid = localStorage.uid;
		const WP_SYNC_TYPES = ['wordpress', 'llvp'];
		if (WP_SYNC_TYPES.includes(get_agenda_sync_type()) && WP_LLVP_AGENDA_SYNC_USER) {
			if (WP_LLVP_AGENDA_SYNC_USER.userID) {
				localStorage.uid = WP_LLVP_AGENDA_SYNC_USER.userID;
				localStorage.uid_auth_from_wp = true;
				if (get_agenda_sync_type() == 'llvp') {
					// This is our secure syncing.  It requires that the Agenda Server
					// has been configured to mirror the WP authentication.
					localStorage.auth_key = WP_LLVP_AGENDA_SYNC_USER.auth;
				} else {
					// This is our less secure syncing. The Agenda Server just stores and
					// retrieves with the supplied userID. These should be salted and hashed
					// so they are not easily guessable.
					localStorage.removeItem('auth_key');
				}
			} else {
				// If our current stored uid is from WP and WP has stopped sending
				// a userID it means the user has logged out.  Handle that here.
				if (localStorage.uid && localStorage.uid_auth_from_wp) {
					// This resets the stored uid.  The user will get a newly generated anonymous id.
					localStorage.removeItem('uid');
					localStorage.removeItem('auth_key');
					localStorage.removeItem('uid_auth_from_wp');

					// This blasts their current favorites from localStorage.
					// Do we want this?  We don't have full confirmation they were previously synced.
					for (var key of Object.keys(localStorage).filter(function(k) { return is_agenda_key(k)})) {
						localStorage.removeItem(key);
						localStorage.removeItem(key + '__ts');
						localStorage.removeItem(key + '__kind');
					}
				}
			}
		}

		if (localStorage.uid != original_uid) {
			// console.log("uid change", localStorage.uid, original_uid);
			// If the ID we are storing favorites under has changed this ensures we will
			// immediately send our local favorites data to the server with the new ID.
			localStorage.unreported_changes = true;
		}

		// console.log(get_agenda_sync_type(), WP_LLVP_AGENDA_SYNC_USER);
		// console.log(localStorage.uid, localStorage.auth_key, localStorage.uid_auth_from_wp);

		// Translate the old style keys:
		// in_agenda_sess123_pap456 -> in_agenda_pap456, in_agenda_pap456__ts, in_agenda_pap456__kind
		// in_agenda_sess123_none -> in_agenda_sess123, in_agenda_sess123__ts, in_agenda_sess123__kind
		check_update_localstorage();

		// setup login button:
		$('#ll_login_form').submit(check_agenda_user_auth);
		reset_auth_form();

		if ($('.post-load').length == 0) {
			show_correct_agenda_buttons();
		}

        window.setInterval(fetch_agenda, get_agenda_interval() * 1000);

        setup_flag_actions();
        setup_date_actions();

		// Check every 1 second for testing:
        // window.setInterval(fetch_agenda, 1 * 1000);

		// fetch when focus changes
		document.addEventListener("visibilitychange", fetch_agenda);

		maintain_agenda();
		start_countdowns();

        $('.popr').popr({
             // 'speed': 300,
             // 'mode': 'top'
        });

		$('.linklings-wp-plugin-contents .filters select').select2();

		// do this before loading promises so we know
		setup_timezone_changes();
		select_current_date();

		if ($('.post-load').length == 0) {
			jQuery('.tablesched').each(function(i, el) {on_load_date_snippet(el)});
		} else {
			jQuery('.tablesched').on('loaded', on_load_event_handler);
		}

		$('.post-load').each(function (i, el) {
			load_date_snippet($(el), 10);
		})

        tryPollModalAutoLaunch();

        window.addEventListener('message', function(event) {
            // Security: verify origin
            // if (event.origin !== 'https://qna.test.sc25.conference-program.com') return;

            console.log('Received message:', event.data);

            const data = event.data;

            if (data.action === 'openQnaModal') {
                // Create and show modal
                const url = data.url;
                launchQnaModal(url, null, true);
            }
        });
	});


})( jQuery );


function on_load_event_handler(e) {
	let date_div = e.target;
	on_load_date_snippet(date_div);
}


function on_load_date_snippet(date_div) {
	let tz_ = get_timezone_preference();
	date_div = jQuery(date_div);

	show_correct_agenda_buttons(date_div);
	date_div.removeClass('post-load');

	// changeDateTime(date_div, tz_);
	// Wait 'till they're all filled
	if (jQuery('.post-load').length > 0) {
		return false;
	}

	jQuery('.tablesched').each(function (i, el) {
		let date_div_ = jQuery(el);
		if (typeof is_agenda_page != 'undefined' && is_agenda_page) {
			agenda_page_setup(date_div_, true);
		} else if (typeof is_happening_now_page != 'undefined' && is_happening_now_page) {
			happening_now_page_setup(date_div_);
		} else {
			// This effectively happens below for the whole page in full_program_filter_on_selectors();
			// And should likely happen after changeDatetime anyway.
			// full_program_page_setup(date_div_);
		}
	})

	changeDateTime(jQuery('html'), tz_);

	if (typeof is_agenda_page != 'undefined' && is_agenda_page) {
		// We have to do this again after the changeDateTime() call.
		hide_non_agenda_items();
		// show_hide_empty_msg();  // This is is done below.
	} else if (typeof is_happening_now_page != 'undefined' && is_happening_now_page) {
		happening_now_all_loaded();
	} else {
		// full program page
		full_program_fill_filters_from_query();
		full_program_filter_on_selectors();
	}

	// Moved here from inside changeDateTime.
	fix_even_odd();
	hide_empty_tables();
	show_hide_empty_msg();
	hide_empty_date_selectors();
}


function setup_timezone_changes() {

	let change_tz_button = jQuery('.tz-link');
	change_tz_button.click(function() {
		jQuery("#timezone_modal").show().find(".outer_container").css("z-index", "99999").css("visibility", "visible");
		return false;
	});

	let tz_select = jQuery('.tz-select');
	// var tz_select = jQuery('.tz_selector_cb');

	tz_select.change( function () {
		newTZ = jQuery(this).val();
		save_timezone_preference(newTZ);

		// We now require a full page reload to handle a change in timezone because
		// we have optimized the page load to only load date slots relevant to the
		// current timezone.
		location.reload();

		// Prior code that updates the page by hiding and showing the date slots.
		// changeDateTime(jQuery('HTML'), newTZ);
		//
		// // Sometimes when switching timezones we were getting a case
		// // when not all agenda items were appear that were suppsed to.
		// // This fixes that by reseting the display of all agenda items.
		// full_program_filter_on_selectors();
		//
		// // Moved here from inside changeDateTime
		// fix_even_odd();
		// hide_empty_tables();
		// show_hide_empty_msg();
		// hide_empty_date_selectors();
		//
		// // Hide the modal
		// jQuery('#timezone_modal').hide().find(".outer_container").css("visibility", "hidden");
		//
		// jQuery(window).trigger('timezone_set');
	});

	startTZ = get_timezone_preference();
	if (tz_select.val() != startTZ) {
		tz_select.val(startTZ);

		// We can't do this here any more since we are reloading the page when a timezone is changed.
		// If this was triggering important setup we'll need to move that elsewhere - but I think
		// that should be happening elsewhere.
		// tz_select.change();
	}
	// if (tz_select.find(':checked').val() != startTZ) {
	// 	tz_select.find('[value="' + startTZ + '"]').attr('checked', true);
	// }

	// I'm not sure we need to do this here -- at least for cases where the program
	// is being loaded via ajax this is premature -- the program hasn't loaded yet.
	changeDateTime(jQuery('HTML'), startTZ);
}


function save_timezone_preference(newTZ) {
	localStorage['tz_preference'] = newTZ;
}


function get_timezone_preference() {
	// returns the stored preference if there is one, otherwise
	// stores the default and returns that.

	let tz = '';

	let tz_selector = jQuery('.tz-select');

	// if we have a hidden input, use that - we aren't letting them choose their tz.
	if (tz_selector.attr('type') == 'hidden') {
		tz = tz_selector.val();
		save_timezone_preference(tz);
		return tz;
	}

	if (localStorage.getItem('tz_preference')) {
		tz = localStorage.getItem('tz_preference');
	}

	// Check if the TZ is valid.
	try {
		Intl.DateTimeFormat(undefined, {timeZone: tz});
		// It's valid - continue.
	}
	catch (ex) {
		// It's invalid
		tz = '';
	}

	// If we don't have one - try to select a valid one from the
	// select list.  We do this after the above validity check to
	// handle cases where an invalid tz value was stored - we can
	// likely still get a valid fallback here.
	if (!tz) {
		tz = tz_selector.val();
		// var tz = jQuery('.tz_selector_cb:checked').val();
	}

	if (tz) {
		save_timezone_preference(tz);
	}

	return tz;
}


function force_select_timezone() {
	// Make them select a timezone and refresh the page.
	// We do this because the schedule page requries a valid timezone to display the schedule.
	// Note that this has been known to create an recursive reloading of the page if we have
	// certain bugs handling valid timezones during page load.  I don't think switching from
	// a full reload to re-running just the setup-js won't fix this because we will still
	// hit the same recursive loop (just within the page).
	// I think we want to move towards removing requiring the user to select a timezone to make
	// the page work and include an explicit setting of the conference timezone as a default - I
	// think this would involved sending the IANA name of the timezone in with all snippets.
	jQuery(window).on('timezone_set', function () {
		if (jQuery('.tz-select').val()) {
			location.reload();
		}
	});
	jQuery('.tz-link').click();
}


function changeDateTime (container, newTZ) {
	// console.time(container);

	if (!newTZ) {
		// We can't change the times if we don't know what the newTZ is.
		// Sometimes we can hit this case before the TZ has been explicitly set.
		// This should be ok because times are written by default in the conference timezone.
		return;
	}

	update_time_filter_timezone(newTZ);
	let newDate = '';

	let hide_wrong_dates = (
		is_full_program_page() |
		(typeof is_agenda_page != 'undefined' && is_agenda_page) |
		(typeof is_happening_now_page != 'undefined' && is_happening_now_page)
	);

	let to_hide = jQuery();
	let to_show = jQuery();
	jQuery(container).find('.dateTimeInfo').each((x, dtInfo) => {

		let $dtInfo = jQuery(dtInfo);

		// Retrieve date/time info from the html object.
		let utcTime = $dtInfo.attr('utc_time');
		let timeFormat = $dtInfo.attr('time_format');
		let dateFormat = $dtInfo.attr('date_format');

		let ans = changeTimeZone(newTZ, utcTime, timeFormat, dateFormat)

		if (hide_wrong_dates) {
			// .tablesched date=2021-11-13
			// hide_el_if_wrong_date($dtInfo, ans[2]);

			// gather all the rows to show / hide
			let rows_ = show_hide_rows_for_el_date($dtInfo, ans[2]);
			if (rows_ != undefined) {
				show_rows = rows_[0];
				hide_rows = rows_[1];
				to_hide = jQuery.merge(to_hide, hide_rows);
				to_show = jQuery.merge(to_show, show_rows);
			}
		}

		// Fill in the new time.
		$dtInfo.text(ans[0]);
		// Change the date variable.
		newDate = ans[1];

	});

	to_hide.addClass('wrong-date');
	to_show.removeClass('wrong-date');

	// Sometimes when switching timezones we were getting a case
	// when not all agenda items were appear that were suppsed to.
	// This fixes that by reseting the display of all agenda items.
	// Update - moving this to be the responsiblity of the caller
	// to avoid duplicate calls of this expensive function.
	// full_program_filter_on_selectors();

	// Update - moving these to be the responsiblity of the caller
	// to avoid duplicate calls.  Note - they are all necessary to
	// re-render the page correctly.
	// fix_even_odd();
	// hide_empty_tables();
	// show_hide_empty_msg();
	// // hide_empty_date_selectors();

	jQuery(container).find('.timezone').each((x, dtInfo) => {
		try {
			changeTZAbbr(dtInfo, newTZ);
		} catch (error) {
			force_select_timezone();
		}
	});

	// Fill in the new date.
	jQuery(container).find('.presentation-date').each((z, dateElement) => {
		jQuery(dateElement).text(newDate);
	});
	// console.timeEnd(container);

	jQuery(window).trigger('timezone_set');
}


function update_time_filter_timezone(newTZ) {
	let time_filt = jQuery('[name=time_filt]');
	if (time_filt.length == 0) {
		return;
	}
	time_filt.find('option').each((i, opt) => {
		let $opt = jQuery(opt);
		let slot = $opt.val();
		if (!slot || slot == 'all' || slot == 'now') {
			return;
		}
		let start_stop = slot.split('|', 2);
		let start = start_stop[0];
		let stop = start_stop[1];
		let start_dt = changeTimeZone(newTZ, start, '%l%P', 'YYYY-MM-DD');
		let stop_dt = changeTimeZone(newTZ, stop, '%l%P', 'YYYY-MM-DD');
		let new_slot = start_dt[0] + ' - ' + stop_dt[0];
		$opt.text(new_slot);
	});
}

function changeTZAbbr(tzElem, newTZ) {

	const tzList = tz;
	let utcTime = jQuery(tzElem).attr('utc_time');

	// Need to get the tz long name from the continent/city tz db name.
	// let tzFullName = new Intl.DateTimeFormat('en-GB', {
	// 	timeZone: newTZ, timeZoneName: 'long'
	// }).format(new Date(utcTime)).split(',')[1].trim();
	let long_formatter = getDateTimeFormat({timeZone: newTZ, timeZoneName: 'long'});
	let tzFullName = long_formatter.format(new Date(utcTime)).split(',')[1].trim();


	// Need to get the GMT offset and format it for the tz library.
	// let getDate = new Intl.DateTimeFormat('en-GB', {
	// 	timeZone: newTZ, timeZoneName: 'short'
	// }).format(new Date(utcTime));
	let short_formatter = getDateTimeFormat({timeZone: newTZ, timeZoneName: 'short'});
	let getDate = short_formatter.format(new Date(utcTime));

	let fullOffsetStr = getDate.split(',')[1].trim()

	if (fullOffsetStr == 'WET') {
		tzAbbr = 'WET';
	} else if (fullOffsetStr == 'AZOST'){
		tzAbbr = 'AZOST';
	} else if (fullOffsetStr == 'EGST') {
		tzAbbr = 'EGST';
	} else if (fullOffsetStr == 'GMT') {
		tzAbbr = 'GMT';
	} else if (fullOffsetStr == 'CET') {
		tzAbbr = 'CET';
	} else if (fullOffsetStr == 'EET') {
		tzAbbr = 'EET';
	} else if (fullOffsetStr == 'WT') {
		tzAbbr = 'WT';
	} else if (fullOffsetStr == 'Z') {
		tzAbbr = 'Z';
	} else {

		let offsetStr = fullOffsetStr.replace('GMT', '');
		let plusMinus = offsetStr[0];
		offsetStr = offsetStr.slice(1);
		let offset = '';

		if (offsetStr.includes(':')) {
			offsetStr = offsetStr.replace(':', '');
		}

		if (offsetStr.length === 1) {
			offset = '0' + offsetStr + '00';
		} else if (offsetStr.length === 2) {
			offset = offsetStr + '00';
		} else if (offsetStr.length === 3) {
			offset = '0' + offsetStr;
		} else {
			offset = offsetStr;
		}

		offset = plusMinus + offset;

		// Use the GMT+/- if there is no abbreviation.
		tzAbbr = fullOffsetStr;
		if (tzList[offset]) {
			newLoc = tzList[offset].find(locationArray => locationArray['name'] === tzFullName);
			if (newLoc) {
				tzAbbr = newLoc['abbr'];
			}
		}
	}

	jQuery(tzElem).text(' ' + tzAbbr);

}


function hide_el_if_wrong_date($el, date_ob) {

	// If we look at end times things end up on the wrong day.
	if ($el.hasClass('end-time')) {
		return;
	}

	let day = date_ob.getDate();
	let table = $el.parents('.tablesched');
	if (table) {
		let wrapper_date = table.attr('date');
		let wrapper_day = Number(wrapper_date.split('-')[2]);
		let row = jQuery($el.parents('.agenda-item')) ;
		// include the slots row that follows
		row = jQuery.merge(row, row.next('.slots-slidedown'));
		if (day != wrapper_day) {
			row.addClass('wrong-date');
		} else {
			row.removeClass('wrong-date');
		}
	}

}


function show_hide_rows_for_el_date($el, date_ob) {

	// If we look at end times things end up on the wrong day.
	if ($el.hasClass('end-time')) {
		return;
	}

	let show_rows = jQuery();
	let hide_rows = jQuery();

	let day = date_ob.getDate();
	let table = $el.parents('.tablesched');
	if (table) {
		let wrapper_date = table.attr('date');
		let wrapper_day = Number(wrapper_date.split('-')[2]);
		let row = jQuery($el.parents('.agenda-item')) ;

		// include the slots row that follows
		// let slots = row.next('.slots-slidedown').find('.agenda_item');
		row = jQuery.merge(row, row.next('.slots-slidedown'));
		// row = jQuery.merge(row, slots);
		if (day != wrapper_day) {
			hide_rows = row;
		} else {
			show_rows = row;
		}
	}

	ans = [show_rows, hide_rows];
	return ans;

}


function hide_empty_date_selectors() {
	jQuery('.date-sels .large-date-sel').each(function(i, el) {
		let selector = jQuery(el);
		let date = selector.attr('date');

		if (date == 'all' | date == 'unscheduled') {
			return;
		}

		let date_disp = jQuery('.date-disp.' + date);

		let session_contents_agenda_items = date_disp.find('.session-contents .agenda-item');
		let wrong_date_agenda_items = date_disp.find('.agenda-item:not(.wrong-date)');
		let top_level_wrong_date_agenda_items = wrong_date_agenda_items.not(session_contents_agenda_items);

		if (top_level_wrong_date_agenda_items.length == 0) {
			selector.addClass('empty-date-sel');
			jQuery('.small_date_sel[date=' + date + ']').addClass('empty-date-sel');
		} else {
			selector.removeClass('empty-date-sel');
			jQuery('.small_date_sel[date=' + date + ']').removeClass('empty-date-sel');
		}

		// if (date_disp.find('.agenda-item').length - date_disp.find('.agenda-item.wrong-date').length <= 0) {
		// 	selector.addClass('empty-date-sel');
		// 	jQuery('.small_date_sel[date=' + date + ']').addClass('empty-date-sel');
		// } else {
		// 	selector.removeClass('empty-date-sel');
		// 	jQuery('.small_date_sel[date=' + date + ']').removeClass('empty-date-sel');
		// }

	});
}


function select_current_date() {
	var curr_date = new Date();
	var month_ = curr_date.getMonth() + 1;
	var date_to_show = curr_date.getFullYear() + '-' + month_.toLocaleString(undefined, {minimumIntegerDigits: 2}) + '-' + curr_date.getDate().toLocaleString(undefined, {minimumIntegerDigits: 2});

	if (jQuery('.' + date_to_show).length > 0) {
		show_date(date_to_show);
	} else {
		show_date("all");
	}
}


var date_sel;


function find_next_date() {
	let curr_date = date_sel.val();
	let next_date_sel = jQuery('.small_date_sel[date=' + curr_date + ']').nextAll(':not(.empty-date-sel)').first();
	let next_date = next_date_sel.attr('date');
	if (next_date == 'next') {
		return curr_date;
	}
	return next_date;
}


function find_prev_date() {
	let curr_date = date_sel.val();
	let prev_date_sel = jQuery('.small_date_sel[date=' + curr_date + ']').prevAll(':not(.empty-date-sel)').first();
	let prev_date = prev_date_sel.attr('date');
	if (prev_date == 'prev') {
		return curr_date;
	}
	return prev_date;
}


function maintain_small_date_sel_arrows() {
	let curr_date = date_sel.val();

	let prev_date_sel = jQuery('.small_date_sel[date=' + curr_date + ']').prevAll(':not(.empty-date-sel)');
	if (prev_date_sel.length <= 1) {
		jQuery('.small_date_sel[date=prev]').removeClass('prev-next');
	} else {
		jQuery('.small_date_sel[date=prev]').addClass('prev-next');
	}

	let next_date_sel = jQuery('.small_date_sel[date=' + curr_date + ']').nextAll(':not(.empty-date-sel)');
	if (next_date_sel.length <= 1) {
		jQuery('.small_date_sel[date=next]').removeClass('prev-next');
	} else {
		jQuery('.small_date_sel[date=next]').addClass('prev-next');
	}
}

function show_date(date) {
	// date_sel is not initialized on all pages, so let's skip this if it's
	// not to avoid an error.
	if (!date_sel) {
		return
	}

	if (date == 'next')	{
		date = find_next_date()
	} else if (date == 'prev') {
		date = find_prev_date()
	}

    date_sel.val(date);

    if (date == 'all') {
        jQuery(".date-disp").show();
        jQuery(".small_date_sel_container").hide().first().show();
    } else {
        jQuery(".date-disp").hide();
        jQuery(".small_date_sel_container").hide();
        jQuery("." + date).show();
    }
    jQuery('.large-date-sels, .small-date-sels').find('*').removeClass('selected-date');
    jQuery('[date=' + date + ']').addClass('selected-date');

    // Focus on the arrow for the next day
    jQuery('.small_date_sel_container:visible').find('.small_date_sel[date=next]').focus();

	maintain_small_date_sel_arrows();

  hide_empty_tables();
	fix_even_odd();
	show_hide_empty_msg();
}


const dateTimeFormatCache = {};
function getDateTimeFormat(options) {
	// Intl.DateTimeFormat is expensive to create, so we cache the results.
	// Create a unique cacheKey by stringifying the options object
	const cacheKey = JSON.stringify(options);
	if (!dateTimeFormatCache[cacheKey]) {
	dateTimeFormatCache[cacheKey] = new Intl.DateTimeFormat('en-US', options);
	}
	return dateTimeFormatCache[cacheKey];
}


let changeTimeZoneCache = {};
function changeTimeZone(newTZ, utc_time, format, dateFormat) {
	let cacheKey = [newTZ, utc_time, format, dateFormat].join('|');

	// Check if the result is in cache
	if(changeTimeZoneCache[cacheKey]) {
		return changeTimeZoneCache[cacheKey];
	}

	// "a.m./p.m." variant: same rendering as long_12_hour_spaced, flagged by a
	// 'periods:' sentinel on the format. Strip it so strftime sees a normal
	// format, and convert the meridiem to periods on the result below.
	let periodsMeridiem = false;
	if (format.startsWith('periods:')) {
		periodsMeridiem = true;
		format = format.slice('periods:'.length);
	}

	// Change the short_12_hour time format if there are minutes.
	let splitUtcTime = utc_time.split(':', 2);
	let mins = splitUtcTime.pop();
	if ((format === '%l%P') && (mins !== '00')) {
		format = '%l:%M%P'
	}

	// Change the date format if it includes day suffixes.
	let dateFormatSuff = '';
	if (dateFormat.endsWith('%-d{S}')) {
		dateFormatSuff = dateFormat;
		dateFormat = dateFormat.replace('{S}', '');
	}

	// Get the base info at UTC for the date and time in question.
	let baseDT = new Date(utc_time);

	let endDT;
	try {
		// This is the date-time for the (new) inputted TZ.

		// toLocalString is very slow.
		// endDT = new Date(baseDT.toLocaleString('en-US', {
		// 	timeZone: newTZ
		// }));

		// This caches the slow part of toLocaleString
		let formatter = getDateTimeFormat({
			timeZone: newTZ,
			// These opts ensure a format readable by Date().
			year: 'numeric',
			month: 'numeric',
			day: 'numeric',
			hour: 'numeric',
			minute: '2-digit',
			second: '2-digit',
		});
		endDT = new Date(formatter.format(baseDT));

	} catch (error) {
		force_select_timezone();
	}

	// Get and parse the formatted date-time using the new tz's time.
	let formattedDT = strftime(dateFormat + ', ' + format, new Date(endDT.getTime()));
	let splitDateTime = formattedDT.split(',');
	let newTime = splitDateTime.pop();
	let newDate = splitDateTime.join(', ');

	// "a.m./p.m." variant: strftime's %P yields "am"/"pm"; add the periods.
	if (periodsMeridiem) {
		newTime = newTime.replace('am', 'a.m.').replace('pm', 'p.m.');
	}

	// Re-format the date if the days need suffixes. (This assumes there is no year.)
	if (dateFormatSuff) {

		let dateArr = newDate.split(',');
		// Keep name of the day as is.
		let dayName = dateArr[0];
		let dayNum = dateArr[1].trim();
		dayNum = dayNum.split(' ');
		// Add suffixes.
		if (dayNum[1] === '1') {
			dayNum[1] += 'st';
		} else if (dayNum[1] === '2') {
			dayNum[1] += 'nd';
		} else if (dayNum[1] === '3') {
			dayNum[1] += 'rd';
		} else if (parseInt(dayNum[1]) > 3) {
			dayNum[1] += 'th';
		}
		// Recompose the date.
		dayNum = dayNum.join(' ').trim();
		newDate = dayName + ', ' + dayNum;
	}

	let result = [newTime, newDate, endDT];

	// Store the result in the cache before returning
	changeTimeZoneCache[cacheKey] = result;

	return result;
}


function date_action_handler(event) {

    if (event.type == 'keydown') {
        var code = event.key; // recommended to use event.key, it's normalized across devices and languages
        if (code != 'Enter') {
            return true;
        }
    }
    var date = jQuery(this).attr('date');

    show_date(date);

	save_filter_opts();

    return true;
}

function setup_date_actions() {
    jQuery(document).on('click', '.small_date_sel, .large-date-sel', date_action_handler);
    jQuery(document).on('keydown', '.small_date_sel, .large-date-sel', date_action_handler);
}


function on_agenda_page() {
    return jQuery('.my_agenda').hasClass('current-page');
}


function load_date_snippet(date_div, tries) {

	if (tries == 0) {
		date_div.html('Could not load schedule for this day');
		return false;
	}

	let date_str = date_div.attr('date'); // format: 2021-11-13
	let src = date_div.attr('source');

	jQuery.ajax({
		url: src,
		uniq_param: (new Date()).getTime(),   // This prevents IE from caching.
		type: 'GET',
		success: function (data) {

			let original_data = data;
			try {
				// Since parsing the full html is expensive, for certain pages that aren't going to be
				// showing everything we can filter the html before parsing it.
				data = filter_date_table_html(date_str, data);
			} catch (error) {
				// Since this is an optimization, we can always fall back to using the full html.
				// This is true for now - but only because we still have the original code that also
				// filters the disp slots after parsing.  We may end up removing that code for simplicity
				// and optimization reasons and then we won't be able to use this fallback.
				console.log("Exception while filtering HTML for parseing", error);
				data = original_data;
			}

			let contents = jQuery('<div>').html(data);
			date_div.html(contents);

			// show_correct_agenda_buttons(contents);  // This is done in jQuery('.tablesched').on('loaded')
			date_div.removeClass('post-load');

			contents.children().unwrap();
			date_div.trigger('loaded');
		},
		error: function () {
			// A failed load almost always means the cached day-snippet file is missing
			// (e.g. the linklings_snippets cache was cleared while the page HTML stayed
			// cached by a page cache like Breeze). In the normal case the file is present
			// and served statically by the web server, so this branch never runs and adds
			// no load. On failure, ask the server to refill the file once, then retry.
			var settings = (typeof LL_PROGRAM_SETTINGS !== 'undefined') ? LL_PROGRAM_SETTINGS : null;
			if (settings && settings.refill_url && !date_div.data('ll_refill_tried')) {
				date_div.data('ll_refill_tried', true);
				var fn = src.split('?')[0].split('/').pop();
				jQuery.ajax({
					url: settings.refill_url,
					type: 'POST',
					data: { fn: fn },
					complete: function () {
						setTimeout(function () {
							load_date_snippet(date_div, tries - 1);
						}, 2000);
					}
				});
			} else {
				setTimeout(function () {
					load_date_snippet(date_div, tries - 1);
				}, 2000);
			}
		}
	});
	return false;
}


function filter_date_table_html(date_str, date_html) {

	// The html returned by ajax requests for date tables includes a superset of the
	// rows that we need to display.  We used to parse the html and then filter
	// the rows, but this can be quite slow.  Here we are filtering the html before
	// parsing it which can significantly speed things up.

	const TABLE_START_MARKER = '<!-- date_disp_table START -->';

	if (date_html && date_html.indexOf(TABLE_START_MARKER) > -1) {
		// console.log("filtering date table html", date_str, date_html.length);

		// const now = new Date();
		let curr_tz = get_timezone_preference();  // user's preferred timezone
		let date_start = date_str + 'T00:00:00';
		let date_start_utc = moment.tz(date_start, curr_tz).utc().format();
		let date_end = moment(date_start_utc).add(1, 'days')
		let date_end_utc = moment.tz(date_end, curr_tz).utc().format();

		// Allow a custom initial now to be passed in via url for the "happening now" page.
		let now_param = new URLSearchParams(window.location.search).get("now");
		let now;
		if (now_param) {
			now = new Date(now_param);
			console.log("Using now param: ", now_param, now);
		} else {
			now = new Date();
		}

		let _is_agenda_page = (typeof is_agenda_page != 'undefined' && is_agenda_page);
		let _is_happening_now_page = (typeof is_happening_now_page != 'undefined' && is_happening_now_page);

		let first = true;

		date_html = filter_disp_rows(date_html, function(disp_row) {

			// 1. Filter Timezones:
			// date_html includes extra disp rows to be able to include any rows that
			// that could on that day in any timezone on earth.  Here we filter out
			// the rows that aren't on the relevant date using the user's preferred
			// timezone.
			const s_utc = (disp_row.match(/s_utc="([^"]*)"/) || [])[1];
			const e_utc = (disp_row.match(/e_utc="([^"]*)"/) || [])[1];
			let in_correct_date_for_tz = (s_utc <= date_end_utc) && (e_utc > date_start_utc);
			if (!in_correct_date_for_tz) {
				return false;
			}

			// 2. Filter Agenda for My Agenda Page:
			// If we are on the my agenda page we can filter out any rows that aren't
			// in the user's agenda.
			if (_is_agenda_page) {
				const psid = (disp_row.match(/psid="([^"]*)"/) || [])[1];
				const ssid = (disp_row.match(/ssid="([^"]*)"/) || [])[1];
				if (!item_in_agenda(psid, ssid)) {
					return false;
				}
			}

			// 3. Filter for Happening Now Page:
			// If we are on the happening now page we can filter out any rows that aren't
			// happening now.  Note that since the happening now page auto-updates what is
			// "happening now" every couple minutes we include the rows for the next 24
			// to make sure this page doesn't go blank if left open (it will go blank if
			// left open for more than 24 hours).

			// Always include the first row to help with nothing_happening_view().
			// Note that this is the first after the previous filters.  Future filters may
			// need some consideration on whether they should be applied before or after this.
			if (_is_happening_now_page) {
				// Always include the first row to help with nothing_happening_view().
				// Note that this is the first after the previous filters.  Future filters may
				// need some consideration on whether they should be applied before or after this.
				if (first) {
					first = false;
					// console.log("Including first row", disp_row);
					return true;
				}

				let start_padding_time = (disp_row.match(/start_padding_time="([^"]*)"/) || [])[1];
				const end_padding_time = (disp_row.match(/end_padding_time="([^"]*)"/) || [])[1];

				// Add additional start padding time (24hr) to have upcoming events remain in the page
				// so that the "next event" message can be displayed correctly and so that we
				// can update the page as time moves forward without having to reload it.
				start_padding_time = (parseInt(start_padding_time) || 30) + (24 * 60);

				let is_happening = event_happening_ts(now, s_utc, e_utc, start_padding_time, end_padding_time);
				if (!is_happening) {
					// console.log(disp_row);
					return false;
				}
			}

			return true;
		});

		// console.log("filtered date table html", date_str, date_html.length);
	}

	return date_html;
}


function filter_disp_rows(date_disp_str, filter_func) {
	const date_disp_data = split_date_disp_str(date_disp_str);
    const filtered_disp_rows = date_disp_data.disp_rows.filter(filter_func);

    const concatenated_str = date_disp_data.date_prefix
        + filtered_disp_rows.join('')
        + date_disp_data.date_suffix;

    return concatenated_str;
}


function split_date_disp_str(date_disp_str) {
    // const delimiter = '<tr class="agenda-item';
	const TABLE_START_MARKER = '<!-- date_disp_table START -->';
	const TABLE_END_MARKER = '<!-- date_disp_table END -->';
	const ROW_START_MARKER = '<!-- slot_disp_row START -->';
	const ROW_END_MARKER = '<!-- slot_disp_row END -->';

    let date_chunks = date_disp_str.split(TABLE_START_MARKER);
	let date_prefix = date_chunks[0];
	date_chunks = date_chunks[1].split(TABLE_END_MARKER);
	let date_body = date_chunks[0];
	let date_suffix = date_chunks[1];

	let disp_rows = date_body.split(ROW_START_MARKER);
	disp_rows.shift(); // Remove the first empty element.

    // Append the ROW_START_MARKER to each chunk, because the split operation removes it.
    for (let i = 0; i < disp_rows.length; i++) {
        disp_rows[i] = ROW_START_MARKER + disp_rows[i];
    }

    return { date_prefix, date_suffix, disp_rows };
}


function event_happening(event_wrapper, now_) {

	var start_ts_utc = event_wrapper.attr('s_utc');
	var end_ts_utc = event_wrapper.attr('e_utc');
	var start_padding = event_wrapper.attr('start_padding_time');
	var end_padding = event_wrapper.attr('end_padding_time');

	return event_happening_ts(now_, start_ts_utc, end_ts_utc, start_padding, end_padding);
}


function event_happening_ts(now_, start_ts_utc, end_ts_utc, start_padding, end_padding) {

	if (typeof start_ts_utc == 'undefined' || typeof end_ts_utc == 'undefined') {
		return false;
	}

	if (typeof start_padding == 'undefined') {
		start_padding = 30;
	} else {
		start_padding = parseInt(start_padding) || 30;
	};

	if (typeof end_padding == 'undefined') {
		end_padding = 30;
	} else {
		end_padding = parseInt(end_padding) || 30;
	};

	var start_ts_ob = new Date(start_ts_utc);
	start_ts_ob.setMinutes(start_ts_ob.getMinutes() - start_padding);
	var end_ts_ob = new Date(end_ts_utc);
	end_ts_ob.setMinutes(end_ts_ob.getMinutes() + end_padding);

	// console.log(now_, start_ts_ob, end_ts_ob);

	if (now_ < start_ts_ob || now_ > end_ts_ob) {
		return false;
	};

	return true;
}


function ____________AGENDA__________() {}


function flag_action_handler(event) {

    if (event.type == 'keydown') {
        var code = event.key; // recommended to use event.key, it's normalized across devices and languages
        if (code != 'Enter') {
            return true;
        }
    }
    var agenda_item = jQuery(this).parents('.agenda-item');
    var psid = agenda_item.attr('psid');
    var ssid = agenda_item.attr('ssid');

    toggle_agenda(psid, ssid);

    return true;
}

function setup_flag_actions() {
    jQuery(document).on('click', '.agenda-button', flag_action_handler);
    jQuery(document).on('keydown', '.agenda-button', flag_action_handler);
}


function toggle_agenda__OLD(psid, ssid) {

	var key = 'in_agenda_' + psid + '_' + ssid;
	var ts_key = key + '__ts';

	// Add (psid, ssid) if it's not there, otherwise remove it.
	if (localStorage[key] != 'true') {
		localStorage[key] = 'true';
	} else {
		localStorage[key] = 'false';
	}

	localStorage[ts_key] = iso_date_no_ms();
	localStorage['unreported_changes'] = 'true';
	show_correct_agenda_button(get_agenda_item(psid, ssid));
}


function report_agenda() {

	if (localStorage.unreported_changes == 'false' || localStorage.unreported_changes == undefined) {
		return jQuery().promise();
	}

	var reporting_url = agenda_reporting_url();

	// Gather the args:
	var conf = jQuery('.linklings-wp-plugin-contents').attr('conference').toLowerCase();
	var event = jQuery('.linklings-wp-plugin-contents').attr('event').toLowerCase();

	if (!conf || !event) {
		return jQuery().promise();
	}

	reporting_url = reporting_url + conf + '/' + event + '/favorites';

	// TODO: how do we want to build unique uids?
	var uid = get_agenda_uid();
	var auth_key = get_agenda_auth_key();

	// add in timestamps for things added/removed from the agenda.
	var sessions = [];
	var presentations = [];
	for (key in localStorage) {

		// Skip non-agenda keys
		if (!is_agenda_key(key)) {
			continue;
		}
		// Make sure it's a reasonable id:
		var id = key.substr(10);
		if (!hasNumber(id)) {
			continue;
		}

		// Build the data
		id_data = {}
		id_data['id'] = id;
		ts_key = key + '__ts';
		id_data['timestamp'] = localStorage[ts_key];
		id_data['value'] = '0';
		if (localStorage[key] == 'true') {
			id_data['value'] = '1';
		}

		var type_key = key + '__kind';

		// We are consolidating all schedule ids into the "sessions" array.
		// Note that we are keeping the "presentations" array in the data but only
		// to maintain backwards compatibility.
		// if (localStorage[type_key] == 'session') {
		// 	sessions.push(id_data);
		// } else {
		// 	presentations.push(id_data)
		// }
		sessions.push(id_data);

	}

	// Note we have consolidated all schedule ids into the "sessions" array.
	// In a future update to the favorites server we would like to move to a
	// v2 that has just one syncable array (e.g., "schedule") and we could
	// have the favorites server handle the two ways of accessing the data.
	var data = {
		'version': iso_date_no_ms(),
		'sessions': sessions,
		'presentations': presentations
	}

	// var start = new Date();
	return jQuery.post({
		"url": reporting_url,
		"contentType": "application/json",
		"headers": {"userID": uid, "Authorization": auth_key},
		"data": JSON.stringify(data),
		"success": function() {
			// var seconds = (new Date() - start) / 1000;
			// console.log('time: ' + seconds + ' seconds\n' + 'success ' + iso_date_no_ms());

			localStorage['last_reported'] = Date.now();
			localStorage['unreported_changes'] = false;
			return true;
		},
		"error": function(jqr, e1, e2) {
			// console.log(e1 + ' ' + e2);
		}
	});
}


function maintain_agenda() {
	return fetch_agenda().done(report_agenda);
}


function fetch_agenda() {

	if (document.visibilityState == 'hidden') {
		return jQuery().promise();
	}

	// console.log('fetching', iso_date_no_ms());
	var reporting_url = agenda_reporting_url();

	// Gather the args:
	var conf = jQuery('.linklings-wp-plugin-contents').attr('conference').toLowerCase();
	var event = jQuery('.linklings-wp-plugin-contents').attr('event').toLowerCase();

	if (!conf || !event) {
		return jQuery().promise();
	}

	reporting_url = reporting_url + conf + '/' + event + '/favorites';

	var uid = get_agenda_uid();
	var auth_key = get_agenda_auth_key();

	// var start = new Date();

	return jQuery.get({
		"url": reporting_url,
		"headers": {"userID": uid, "Authorization": auth_key},
		"success": function(data) {
			// var seconds = (new Date() - start) / 1000;
			// console.log('time: ' + seconds + ' seconds');
			merge_server_data(data);
			show_correct_agenda_buttons();
			if (on_agenda_page()) {
				// jQuery('.date-disp').show();
				hide_non_agenda_items();
				empty_agenda_view();
			}
		},
		"error": function(jqr, e1, e2) {
			// console.log(e1 + ' ' + e2);
		}
	});
}


function merge_server_data(data) {

	// Note we have consolidated all schedule ids into the "sessions" array.
	// However the favorites server doesn't know about this - so any presentations
	// previously saved in the presentations array will continue to be returned
	// there by the favorites server.  This routine has been updated to handle
	// presentations or session being returned in either of the "presentations" or
	// "sessions" arrays.
	// In a future update to the favorites server we would like to move to a
	// v2 that has just one syncable array (e.g., "schedule") and we could
	// have the favorites server handle the two ways of accessing the data.

	var sessions = data['sessions'];
	for (i in sessions) {
		var psid_data = sessions[i];
		var psid = psid_data['id'];
		var ls_key = 'in_agenda_' + psid;

		// We are consolidating all schedule favorites into the "sessions" array.
		//  allows us to correctly read both sessions and presentations from this array.
		let schedule_type = schedule_type_of_id(psid);

		if (localStorage.getItem(ls_key) !== null) {
			var ls_ts_key = ls_key + '__ts';
			if (localStorage.getItem(ls_ts_key) < psid_data['timestamp']) {
				store_agenda_item(
					psid,
					psid_data['timestamp'],
					psid_data['value'],
					schedule_type
				)
			}
		} else {
			store_agenda_item(
				psid,
				psid_data['timestamp'],
				psid_data['value'],
				schedule_type
			)
		}
	}

	var presentations = data['presentations'];
	for (i in presentations) {
		var ssid_data = presentations[i];
		var ssid = ssid_data['id'];
		var ls_key = 'in_agenda_' + ssid;

		// We are consolidating all schedule favorites into the "sessions" array.
		// For backwards compatibility we still want to read what is stored in the
		// presentations array.  This is now handling it as if it were a contactenation
		// of the sessions array.
		let schedule_type = schedule_type_of_id(ssid);

		if (localStorage.getItem(ls_key) !== null) {
			var ls_ts_key = ls_key + '__ts';
			if (localStorage.getItem(ls_ts_key) < ssid_data['timestamp']) {
				store_agenda_item(
					ssid,
					ssid_data['timestamp'],
					ssid_data['value'],
					schedule_type
				)
			}
		} else {
			store_agenda_item(
				ssid,
				ssid_data['timestamp'],
				ssid_data['value'],
				schedule_type
			)
		}
	}
}


function schedule_type_of_id(id_) {
	if (is_session(id_)) {
		return 'session';
	} else {
		return 'presentation';
	}
}


const session_re = /^sess\d+$/;

function is_session(id_) {
	// The session id_prefix is hardcoded in psess_db.
	return session_re.test(id_);
}


function store_agenda_item(id, timestamp, value, agenda_kind) {

	var ls_key = 'in_agenda_' + id;
	var ls_ts_key = ls_key + '__ts';
	var ls_kind_key = ls_key + '__kind';

	if (value == '1' || value == 'true') {
		localStorage[ls_key] = 'true';
	} else {
		localStorage[ls_key] = 'false';
	}
	localStorage[ls_ts_key] = timestamp;
	localStorage[ls_kind_key] = agenda_kind;
}


function toggle_agenda(psid, ssid) {

	var key = '';
	var event_kind = ''
	if (ssid == 'none') {
		key = 'in_agenda_' + psid;
		event_kind = 'session';
	} else {
		key = 'in_agenda_' + ssid;
		event_kind = 'presentation'
	}

	// Add (psid, ssid) if it's not there, otherwise remove it.
	if (localStorage[key] != 'true') {
		localStorage[key] = 'true';

		try {
			WonderPush.push(() => {
				WonderPush.trackEvent('SESSION_ADDED', {string_name: psid});
			});
		} catch(error) {}

	} else {
		localStorage[key] = 'false';

		try {
			WonderPush.push(() => {
				WonderPush.trackEvent('SESSION_REMOVED', {string_name: psid});
			});
		} catch(error) {}
	}

	var ts_key = key + '__ts';
	var kind_key = key + '__kind';

	localStorage[ts_key] = iso_date_no_ms();
	localStorage[kind_key] = event_kind;
	localStorage['unreported_changes'] = 'true';

	report_agenda();

	show_correct_agenda_button(get_agenda_item(psid, ssid), true);
}


function get_page_items_not_in_agenda() {

	// Note that this only gets agenda items that are currently in the page.

	var all_agenda_items = jQuery('.agenda-item');
	var non_agenda_items = jQuery();
	all_agenda_items.each(function (i, el) {
		var psid = jQuery(el).attr('psid');
		var ssid = jQuery(el).attr('ssid');
		if (!item_in_agenda(psid, ssid)) {
			non_agenda_items = non_agenda_items.add(jQuery(el))
		}
	});
	return non_agenda_items;
}


function get_page_items_in_agenda() {

	// Note that this only gets agenda items that are currently in the page.
	// When we start reporting back to the server the list of items we'll have to send the whole list from localStorage.

	return jQuery('.agenda-item.in_agenda'); // Optimization.

	// var all_agenda_items = jQuery('.agenda-item');
	// var agenda_items = jQuery();
	// all_agenda_items.each(function (i, el) {
	// 	var psid = jQuery(el).attr('psid');
	// 	var ssid = jQuery(el).attr('ssid');
	// 	if (item_in_agenda(psid, ssid)) {
	// 		agenda_items = agenda_items.add(jQuery(el));
	// 	}
	// });
	// return agenda_items;
}


function ____________PERSISTANT_FILTERS__________() { }

//const ORIGINAL_FILTER_BAR = true;

//this variable is now set by wp_snippets.py. It can be "off", "bottom", or "top"

//if you have old snippets, the variable won't have been declared via the snippets
if (typeof STICKY_FILTER_BAR_TYPE == 'undefined') {
	STICKY_FILTER_BAR_TYPE = 'bottom';
}


function save_filter_opts() {
	let selects = jQuery.merge(jQuery('.filter-select'), jQuery('[name=date_sel]'));
	selects.each(function(){
		let sel = jQuery(this);
		let storage_key = this.name;
		let selected = [];

		// Check if this is a select element or checkbox group
		if (sel.get(0).nodeName.toLowerCase() == 'select') {
			// Handle select elements
			sel.find(':selected').each(function() {
				selected.push(jQuery(this).val());
			});
		} else {
			// Handle checkbox groups - find all checked checkboxes with the same name
			let name = sel.attr('name');
			jQuery("input[name='" + name + "']:checked").each(function() {
				selected.push(jQuery(this).val());
			});
		}

		window.sessionStorage[storage_key] = JSON.stringify(selected);
	})
}


function load_filter_opts() {
	// TODO : what if there is no value?
	let selects = jQuery.merge(jQuery('.filter-select'), jQuery('[name=date_sel]'));
	selects.each(function () {
		let sel = jQuery(this);
		let storage_key = this.name;
		let val = window.sessionStorage[storage_key];

		if (val) {
			let selectedValues = JSON.parse(val);

			// Check if this is a select element or checkbox group
			if (sel.get(0).nodeName.toLowerCase() == 'select') {
				// Handle select elements
				for (let v of selectedValues) {
					sel.find('option[value="' + v + '"]').attr('selected', true);
				}
				sel.trigger('change');
			} else {
				// Handle checkbox groups - find all checkboxes with the same name
				let name = sel.attr('name');
				for (let v of selectedValues) {
					jQuery("input[name='" + name + "'][value='" + v + "']").prop('checked', true);
				}
				// Trigger change on the first checkbox to notify of changes
				jQuery("input[name='" + name + "']:first").trigger('change');
			}
		}
	})
}


function update_filter_display() {

	if (!is_full_program_page()) {
		return false;
	}

	if (STICKY_FILTER_BAR_TYPE === "bottom") {
		//  This won't do anything if there is one already.
		filt_disp = make_filter_display();

		jQuery('.sticky_filter_display').find('.filter_disp_container').empty();
	}

	jQuery('.filter-select').each(function () {
		add_selected_options_for_filter(jQuery(this));
	});

	if (STICKY_FILTER_BAR_TYPE === "bottom") {
		jQuery('.filter_counter').text(' (' + jQuery('.sticky_filter_display .current_filter_val').length + ')')

		show_hide_filter_display();
	}

	if (STICKY_FILTER_BAR_TYPE === "top") {
		jQuery('.filter_counter').text(' (' + jQuery('.filters .select2-selection__choice').length + ')')

		update_top_sticking_filters();
	}
}


function show_hide_filter_display() {
	let filt_disp = jQuery('.sticky_filter_display');

	if (filt_disp.find('.current_filter_val').length == 0) {
		filt_disp.hide(500);
	} else {
		filt_disp.show(250, auto_hide_filter_bar);
	}
}


function auto_hide_filter_bar() {
	let filt_bar = jQuery('.filters_box');
	if (!filter_bar_is_user_shown()) {
		window.setTimeout(function() {
			filt_bar.hide(500);
		}, 1000)
	}
}


function mark_filter_bar_user_shown() {
	let filt_bar = jQuery('.filters_box');
	if (filt_bar.css('display') != 'none') {
		filt_bar.attr('user_shown', 'yes');
	} else {
		clear_filter_bar_user_shown();
	}
}


function clear_filter_bar_user_shown() {
	let filt_bar = jQuery('.filters_box');
	filt_bar.attr('user_shown', 'no');
}


function filter_bar_is_user_shown() {
	let filt_bar = jQuery('.filters_box');
	if (filt_bar.attr('user_shown') == 'yes') {
		return true;
	}
	return false;
}


function toggle_filters_user_shown() {
	filters.toggle(500);
	filters_user_shown = !filters_user_shown;
}


function check_filters_onscreen() {
	if (jQuery(window).scrollTop() > filter_display_top + filter_display_height) {
		return false;
	}
	return true;
}

//This function is only for the filters that stick to the top. It will only be called if STICKY_FILTER_BAR_TYPE is set to "top"
function update_top_sticking_filters() {
	filter_display_top = filter_display.offset().top;
	filter_display_height = filter_display.outerHeight();

	if (check_filters_onscreen()) {
		filter_display.css('min-height', '0px');
		filters.show();
		filters_tab.hide();
		filters_box.removeClass("sticky");
		filters.removeClass("sticky");
	}

	else {
		if (filter_display.css('min-height') === '0px') {
			filter_display.css('min-height', filter_display_height);
		}

		filters_box.addClass("sticky");
		filters.addClass("sticky");

		filters_box.width(filter_display.width());

		if (filters_user_shown) {
			filters_tab.show();
			if (filters.css('overflow') != 'hidden') {
				//This is so that the height of the filter_display div, which stays onscreen, will be adjusted when a filter is added or removed.
				//This keeps the page from jumping when the user scrolls back up.
				filter_display.css("min-height", filters.height());
			}
			if (onscreen != check_filters_onscreen()) {
				filters.hide();
				filters.show(500);
			}
		}

		else {
			if (filters.css('overflow') != 'hidden') { //This is to detect if the filter is being animated.
				filters.hide();
			}
			filters_tab.show();
		}
	}
	onscreen = check_filters_onscreen();
}


function is_in_viewport(el) {
	var elementTop = jQuery(el).offset().top;
	var elementBottom = elementTop + jQuery(el).outerHeight();

	var viewportTop = jQuery(window).scrollTop();
	var viewportBottom = viewportTop + jQuery(window).height();

	return elementBottom > viewportTop && elementTop < viewportBottom;
}


function add_selected_options_for_filter(filter_el) {
	var disp = jQuery('.sticky_filter_display');
	var filter_container = disp.find('[filter=' + filter_el.attr('name') + ']');

	filter_el.find('option:selected').each(function () {
		var opt = jQuery(this);
		var val = opt.val();
		if (val != 'all' && (disp.find('[value=' + val + ']').length < 1 || !(STICKY_FILTER_BAR_TYPE === "bottom"))) {
			var opt_label = opt.text();
			var new_filt_val = jQuery('<div>');
			new_filt_val.addClass('current_filter_val');
			new_filt_val.addClass(filter_el.attr("name"));
			new_filt_val.text(opt_label);
			new_filt_val.attr('value', val);
			new_filt_val.attr('filter', filter_el.attr("name"));
			var remove_icon = jQuery(' <i class="fa fa-times-circle filter-remove-icon"></i>');
			new_filt_val.prepend(remove_icon);
			if (STICKY_FILTER_BAR_TYPE === "bottom") {
				filter_container.append(new_filt_val);
			}
		}

	})
}


function handle_remove_event() {
	var el = jQuery(this);
	remove_selected_from_filter(el);
}


function remove_selected_from_filter(el) {
	var val = el.attr('value');
	var select_name = el.attr('filter');
	var select = jQuery('[name=' + select_name + ']');
	select.find('[value=' + val + ']').removeAttr("selected");
	select.change();
	if (STICKY_FILTER_BAR_TYPE === "bottom") {
		show_hide_filter_display();
	}
}


function remove_all_from_filters() {
	jQuery('.filter-select').find(':selected').each(function(i, el) {
		el.selected = false;
	}).change();
	if (STICKY_FILTER_BAR_TYPE === "bottom") {
		clear_filter_bar_user_shown();
	}
	jQuery('.filters_box').show();
}


function make_filter_display() {

	var filter_disp = jQuery('.sticky_filter_display');
	if (filter_disp.length > 0) {
		return filter_disp;
	}

	var filter_disp = jQuery('<div>').addClass('sticky_filter_display');
	var filter_box_wrapper = jQuery('<div>').addClass('filters_box_wrapper');
	var filter_box = jQuery('<div>').addClass('filters_box');
	var filter_tab = jQuery('<div>').text('Filters ').addClass('sticky_filter_label');
	filter_tab.append(jQuery('<span>').addClass('filter_counter'));

	filter_tab.on('click', function() {
		filter_box.toggle(500);
		mark_filter_bar_user_shown();
	})

	jQuery('body').append(filter_disp);

	filter_disp.append(filter_tab);
	// filter_disp.append(filter_box);
	filter_box_wrapper.append(filter_box);
	filter_disp.append(filter_box_wrapper);
	jQuery('.filter-select').each(function() {
		var filter_name = jQuery(this).attr('name');
		var filter_container = jQuery('<div>').addClass('filter_disp_container').attr('filter', filter_name);
		// filter_disp.append(filter_container);
		filter_box.append(filter_container);
	})

	let clear_button = jQuery('<button>clear all</button>').addClass('clear_filters_button');
	clear_button.on('click', remove_all_from_filters);
	let button_wrapper = jQuery('<div>').addClass('clear_filters_button_wrapper');
	button_wrapper.append(clear_button);
	filter_box.append(button_wrapper);

	filter_disp.css('z-index', '10000');
	filter_disp.hide();

	return filter_disp;
}


function check_update_localstorage() {

	var found_timestamp = false;
	for ( var i = 0, len = localStorage.length; i < len; i++ ) {
		var k = localStorage.key( i );
		if (k.indexOf('__ts') != -1) {
			found_timestamp = true;
		}
	}

	if (found_timestamp) {
		return true;
	}

	var rel_keys = [];
	for ( var i = 0, len = localStorage.length; i < len; i++ ) {
		var key = localStorage.key( i );

		if (is_agenda_key(key)) {
			rel_keys.push(key)
		}
	}

	for ( var i = 0, len = rel_keys.length; i < len; i++ ) {
		var key = rel_keys[i];
		var psid_ssid_pair = key.substr(10).split('_');
		psid = psid_ssid_pair[0];  // psids do not have underscores in their ids.
		// ssid = psid_ssid_pair[1];
		ssid = psid_ssid_pair.slice(1).join('_');  // ssids might have underscores.
		// valid ids have numbers in them.
		// It's only an old agenda item if it has two ids.
		if (hasNumber(psid) && !(ssid == undefined || ssid == '')) {
			var new_key = '';
			var kind = '';
			if (ssid == 'none') {
				new_key = 'in_agenda_' + psid;
				kind = 'session';
			} else {
				new_key = 'in_agenda_' + ssid;
				kind = 'presentation';
			}
			localStorage[new_key] = localStorage[key];
			// we don't have a timestamp so just put now in.
			ts_key = new_key + '__ts';
			localStorage[ts_key] = iso_date_no_ms();
			kind_key = new_key + '__kind';
			localStorage[kind_key] = kind;

			// Delete the outdated key
			localStorage.removeItem(key);
		}
	}

	// make sure we report the changes.
	localStorage['unreported_changes'] = true;
}


function ____________LOGIN___________() {}


function check_agenda_user_auth(event) {

	event.preventDefault();
	// jQuery("#lookup-out").html('updating...');

	jQuery('#ll_login_form #login_success').hide();
	jQuery('#ll_login_form #login_fail').hide();

	var req_pass = jQuery('#ll_login_box').attr('req_pass') == 'true';

	var orig_user_id = get_agenda_uid();

	var user_id = jQuery('#ll_uid').val();
	var auth_key = '';

	if (req_pass) {
		auth_key = jQuery('#ll_authkey').val().trim();
		if (auth_key === '') {
			jQuery('#ll_login_form #login_fail').show();
			jQuery('#ll_authkey').val('');
			return jQuery().promise();
		}
	}
	// var start = new Date();

	var conf = jQuery('.linklings-wp-plugin-contents').attr('conference').toLowerCase();
	var event = jQuery('.linklings-wp-plugin-contents').attr('event').toLowerCase();
	var reporting_url = agenda_reporting_url();
	reporting_url = reporting_url + conf + '/' + event + '/favorites';

	return jQuery.get({
		"url": reporting_url,
		"headers": {"userID": user_id, "Authorization": auth_key},
		"success": function(data) {
			localStorage.uid = user_id;
			localStorage.auth_key = auth_key;
			localStorage.logged_in = true;
			localStorage.unreported_changes = true;

			jQuery('#ll_login_form #logged_in_name_display').hide();
			jQuery('#ll_login_form #ll_login_box').hide();
			jQuery('#ll_login_form #login_success').show();

			// var seconds = (new Date() - start) / 1000;
			// console.log('time: ' + seconds + ' seconds\n');

			if (orig_user_id != user_id) {
				remove_old_user(orig_user_id);
			}

			maintain_agenda().done(function() {
				if (on_agenda_page()) {
					// jQuery('.datate-disp').show();
					hide_non_agenda_items();
					empty_agenda_view();
					show_hide_empty_msg();
				}
			});
		},
		"error": function(jqr, e1, e2) {
			// console.log(e1 + ' ' + e2);
			jQuery('#ll_login_form #login_fail').show();
			jQuery('#ll_authkey').val('');
		}
	});
}


function stop_syncing() {
	localStorage.logged_in = false;
	report_agenda().done(function() {
		localStorage.clear();
		reset_auth_form();
		if (on_agenda_page()) {
			// jQuery('.date-disp').show();
			hide_non_agenda_items();
			empty_agenda_view();
			show_hide_empty_msg();
		}
	});
}


function reset_auth_form() {

	jQuery('#login_modal').hide().find(".outer_container").css("visibility", "hidden");
	jQuery('#ll_login_form #ll_login_box').show();
	jQuery('#ll_login_form #login_success').hide();
	jQuery('#ll_login_form #login_fail').hide();

	// Use get_agenda_uid() rather than reading localStorage directly so a new browser ID
	// is generated when one is missing (e.g. after "stop syncing" clears localStorage).
	jQuery('#ll_login_form #browser_uid').html(get_agenda_uid());
	if (localStorage.getItem('logged_in')) {
		jQuery('#ll_login_form #current_login_name').html(localStorage.getItem('uid'));
		jQuery('#ll_login_form #logged_in_name_display').show();
		jQuery('.logout-link').show();
		jQuery('.login-link').hide();
	} else {
		jQuery('#ll_login_form #logged_in_name_display').hide();
		jQuery('.logout-link').hide();
		jQuery('.login-link').show();
	}
	jQuery('#ll_uid').val('');
	jQuery('#ll_authkey').val('');

}


function remove_old_user(user_id) {

	var conf = jQuery('.linklings-wp-plugin-contents').attr('conference').toLowerCase();
	var event = jQuery('.linklings-wp-plugin-contents').attr('event').toLowerCase();
	var reporting_url = agenda_reporting_url();
	reporting_url = reporting_url + conf + '/' + event + '/remove_anon_user';

	jQuery.post({
		"url": reporting_url,
		"headers": {"userID": user_id},
		"success": function(data) {
			// console.log('removed ' + user_id);
		},
		"error": function(jqr, e1, e2) {
			// console.log(e1 + ' ' + e2);
		}
	});
}

function ____________HELPERS_________() {}


function find_intersection(array1, array2) {
    var ans = jQuery();
    array1.each(function(i, el) {
        if (jQuery.inArray(el, array2) != -1) {
            ans.push(el);
        }
    })
    return ans;
}


function hasNumber(myString) {
  return /\d/.test(myString);
}


function getRandomInt(max) {
	return Math.floor(Math.random() * max);
}


function diff_timestamps_in_minutes(ts1, ts2) {
	var diff_ms = ts1 - ts2;
	var diff_secs = diff_ms / 1000.0;
	var diff_mins = diff_secs / 60;
	return diff_mins;
}


function iso_date_no_ms() {
	var ans = new Date().toISOString();
	ans = ans.substr(0,19) + 'Z';
	return ans;
}


function is_agenda_key(key) {

	// returns true if <key> is an in_agenda flag and not a timestamp or event kind (or anything else).

	if (key.indexOf('in_agenda_') == -1) {
		return false;
	}
	if (key.indexOf('__ts') != -1) {
		return false;
	}
	if (key.indexOf('__kind') != -1) {
		return false;
	}
	return true;
}


function get_agenda_item(psid, ssid) {
	return jQuery('[ssid=' + ssid + ']' + '[psid=' + psid + ']');
}


// function item_in_agenda(psid, ssid) {
// 	var key = 'in_agenda_' + psid + '_' + ssid;
// 	return localStorage[key] == 'true';
// }

function item_in_agenda(psid, ssid) {

	var key = '';
	if (ssid == 'none') {
		key = 'in_agenda_' + psid;
	} else {
		key = 'in_agenda_' + ssid;
	}

	return localStorage[key] == 'true';
}


function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
}


function setQueryVariable(url, variable, value) {
	var query = url.substring(url.indexOf('?') + 1);
	var vars = query.split('&');
	var new_query = '';
	var found = false;
	for (var i = 0; i < vars.length; i++) {
		var pair = vars[i].split('=');
		if (decodeURIComponent(pair[0]) == variable) {
			new_query += variable + '=' + value;
			found = true;
		} else {
			new_query += vars[i];
		}
		if (i < vars.length - 1) {
			new_query += '&';
		}
	}
	if (!found) {
		new_query += '&' + variable + '=' + value;
	}
	return url.substring(0, url.indexOf('?') + 1) + new_query;
}


function get_agenda_interval() {

	// Returns the integer in seconds that we should wait between
	// polling agenda server for changes.

	var content_wrapper_div = jQuery('.linklings-wp-plugin-contents');
	var interval = content_wrapper_div.attr('agenda_interval');

	var int_interval = parseInt(interval);
	if (isNaN(int_interval)) {
		// What's a good default?
		int_interval = 10;
	}

	return int_interval;
}


function get_agenda_sync_type() {
	var content_wrapper_div = jQuery('.linklings-wp-plugin-contents');
	var sync_type = content_wrapper_div.attr('agenda_sync_type');
	return sync_type || 'off';
}


function agenda_reporting_url() {
	var content_wrapper_div = jQuery('.linklings-wp-plugin-contents');
	var staging = content_wrapper_div.attr('staging');

	local_ans = 'http://127.0.0.1:5000/';
	staging_ans = 'https://z32xe7og6d.execute-api.us-west-2.amazonaws.com/dev/'
	live_ans = 'https://grjvpue6x4.execute-api.us-west-2.amazonaws.com/prod/';

	ans = live_ans;
	if (staging == 'yes') {
		// ans = local_ans;
		ans = staging_ans;
	}

	return ans
}


function get_agenda_uid() {

	var uid = localStorage.uid;
	if (!uid) {
		uid = Date.now();
		localStorage['uid'] = uid
	}

	return uid;
}


function get_agenda_auth_key() {

	var auth_key = localStorage.auth_key;
	if (!auth_key) {
		auth_key = ''
	}

	return auth_key;
}


function ____________DISPLAY_________() {}


function fix_even_odd() {

	var odds = jQuery();
	var evens = jQuery();

	jQuery('.tablesched').each(function(i, el) {
		var sched_el = jQuery(el);
		sched_el.find('tr.agenda-item:visible').each(function(j, el) {
			if (j === 0 || !!(j && !(j%2))) {
				// jQuery(el).removeClass('odd').addClass('even');
				evens = evens.add(el);
			} else {
				// jQuery(el).removeClass('even').addClass('odd');
				odds = odds.add(el);
			}
		});
	});

	// Give the slots-slidedown rows the same EO classes as the presentation rows
	jQuery.merge(evens, evens.next('.slots-slidedown'));
	jQuery.merge(odds, odds.next('.slots-slidedown'));

	evens.removeClass('odd').addClass('even');
	odds.removeClass('even').addClass('odd');
}


function hide_empty_tables() {
    var dates = jQuery('.date-disp');
    var selected_date = jQuery('[name=date_sel]').val();
    if (selected_date == 'all') {
        dates.show();
    } else {
        jQuery('.date-disp.' + selected_date).show();
    }
    dates.each(function(i, el) {
		var sched_box = jQuery(el).find('.tablesched');
		if (!sched_box.hasClass('post-load')) {
	        var pres_rows = jQuery(el).find('.presentation-row:visible');
	        if (pres_rows.length == 0) {
	            jQuery(el).hide();
	        }
		}
    });
}


function show_hide_empty_msg() {
    var nothing_in_agenda = jQuery('#empty_agenda_div');
    var nothing_in_display = jQuery('#no-session-msg');

	if (typeof is_happening_now_page != 'undefined' && is_happening_now_page) {
		nothing_in_agenda.hide();
		nothing_in_display.hide();
		return;
	}

	var using_empty_msg;
    var other_empty_msg;

    if (!on_agenda_page()) {
        using_empty_msg = nothing_in_display;
        other_empty_msg = nothing_in_agenda;
    } else {
        if (get_page_items_in_agenda().length == 0) {
            using_empty_msg = nothing_in_agenda;
            other_empty_msg = nothing_in_display;
        } else {
            using_empty_msg = nothing_in_display;
            other_empty_msg = nothing_in_agenda;
        }
    }

    // We don't want to show this because it's not currently applicable.
    other_empty_msg.hide();

    if (jQuery('.spinner:visible').length == 0 && jQuery('.presentation-row:visible').length == 0) {
        using_empty_msg.show();
    } else {
        using_empty_msg.hide();
    }
}


function update_agenda_item_class(el, set_focus) {
    var $el = jQuery(el);
    var psid = $el.attr('psid');
    var ssid = $el.attr('ssid');

    if (item_in_agenda(psid, ssid)) {
        $el.addClass('in_agenda');
		if (set_focus) {
			$el.find('.agenda-add-button').focus();
		}

    } else {
        $el.removeClass('in_agenda');
    }
}


function show_correct_agenda_button(el, set_focus) {

	// Optimization: updating classes and using css to show/hide buttons is faster than
	// using jQuery's show/hide functions.
	update_agenda_item_class(el, set_focus);

	// var psid = jQuery(el).attr('psid');
	// var ssid = jQuery(el).attr('ssid');
    // var show_el;
	// if (item_in_agenda(psid, ssid)) {
	// 	jQuery(el).find('.agenda-add-button').hide();
	// 	show_el = jQuery(el).find('.agenda-remove-button');
	// } else {
	// 	jQuery(el).find('.agenda-remove-button').hide();
	// 	show_el = jQuery(el).find('.agenda-add-button');
	// }
    // show_el.show();
    // if (set_focus) {
    //     show_el.focus();
    // }
}


function update_agenda_items_classes(container) {
    var all_agenda_items;
    if (container == undefined) {
        all_agenda_items = jQuery('.agenda-item');
    } else {
        all_agenda_items = container.find('.agenda-item');
    }
    all_agenda_items.each(function (i, el) {
        update_agenda_item_class(el);
    });
}


function show_correct_agenda_buttons(container) {

	// Optimization: updating classes and using css to show/hide buttons is faster than
	// using jQuery's show/hide functions.
	return update_agenda_items_classes(container);

	// var all_agenda_items;
	// if (container == undefined) {
	// 	all_agenda_items = jQuery('.agenda-item');
	// } else {
	// 	all_agenda_items = container.find('.agenda-item');
	// }
	// all_agenda_items.each(function (i, el) {
	// 	show_correct_agenda_button(jQuery(el));
	// });
}


function show_visible_session_slidedowns(dtd) {

	var visible_sessions = [];
	var date_selector = '';
	if (dtd != undefined) {
		date_selector = '.' + dtd;
	}
	jQuery(date_selector + '.date-disp .presentation-row[ssid=none]:visible').each(function() {
		visible_sessions.push('.slots-slidedown.' + jQuery(this).attr('psid'));
	});

	var slidedowns = jQuery(date_selector + '.date-disp').find(visible_sessions.join(','));
	slidedowns.show().find('.session-display>div').show();
}


function hide_visible_session_slidedowns() {
	// each link controls all the dates.
	// Add dtd like in show_visible_session_slidedowns() to change.
	jQuery('.date-disp .slots-slidedown').hide().find('.session-display>div').hide();
}


function hide_empty_date_containers() {
	jQuery('.date-disp').each(function(i, el) {
		var el_ob = jQuery(el);
		var sched_box = el_ob.find('.tablesched');
		// don't hide ones that are still loading
		if (!sched_box.hasClass('post-load')) {
			var visible_rows = jQuery(el).find('.agenda-item:visible');
			if (visible_rows.length == 0) {
				el_ob.hide();
			} else {
				el_ob.show();
			}
		}
	});

}


function hide_non_agenda_items(container, skip_cleanup) {

	// hide the rows
	// jQuery('.agenda-item').hide();

	let all_agenda_items;
	if (container == undefined) {
		all_agenda_items = jQuery('.agenda-item');
	} else {
		all_agenda_items = container.find('.agenda-item');
	}

	all_agenda_items.hide().removeClass('ll-visible').addClass('ll-not-in-agenda');;

	let agenda_items = get_page_items_in_agenda();
	agenda_items.show().css('display', '').addClass('ll-visible').removeClass('ll-not-in-agenda');

	// We don't need to do this here because hide_empty_date_containers() handles this.
	// let selected_date = jQuery('.selected-date').attr('date')
	// for (var i = 0; i < agenda_items.length; i++) {
	// 	let item_ = jQuery(agenda_items[i]);
	// 	item_.show();
	// 	// If dates have been hidden because they were empty show them again.
	// 	let item_date_div = item_.parents('.tablesched');
	// 	if (selected_date == 'all' | selected_date == item_date_div.attr('date')) {
	// 		item_date_div.parents('.date-disp').show()
	// 	}
	// }

	if (!skip_cleanup) {
		hide_empty_date_containers();
		fix_even_odd();
	}
}


function __________FULL_PROGRAM_PAGE_TOOLS____() {}


function full_program_fill_filters_from_query() {
	var found_filter_opts = false;

	var event_type = getQueryVariable('event_type');
	var orig_etype_val = jQuery('[name=etype_filt]').val();
	if (event_type != undefined) {
		jQuery('[name=etype_filt]').val(event_type);
		found_filter_opts = true;
	} else if (orig_etype_val == undefined) {
		jQuery('[name=etype_filt]').val('all');
	}

    var filters = jQuery('.filter-select');
    for (var i = 0; i < filters.length; i++) {
    	var filt_val = getQueryVariable('filter' + (i + 1).toString());
		var orig_filt_val = jQuery(filters[i]).val();
    	if (filt_val != undefined) {
    		jQuery(filters[i]).val(filt_val);
			found_filter_opts = true;
		} else if (orig_filt_val == undefined) {
    		jQuery(filters[i]).val('all');
    	}
    }

	var date = getQueryVariable('date');
	if (date != undefined) {
		// Do we want to count this as a filter opt?
		// found_filter_opts = true;
		var date_div = jQuery('.date-disp.' + date);
		if (date == 'all' || date_div.length > 0) {
			show_date(date);
		}
	}

	if (found_filter_opts) {
		full_program_filter_event_handler();
		filters.change();
	}

	return found_filter_opts;
}


function full_program_page_setup(container) {
    fix_even_odd();
    full_program_filter_on_selectors(container);
    // show_hide_empty_msg();
}


function full_program_filter_rows_on_etype(etype) {
    if (etype == 'all') {
        return jQuery('.presentation-row');
    } else {
        return jQuery('.presentation-row[etypes*=' + etype + ']');
    }
}


function full_program_filter_rows_on_ptrack(ptrack) {
    if (ptrack == 'all') {
        return jQuery('.presentation-row');
    } else {
        return jQuery('.presentation-row[ptracks*=' + ptrack + ']');
    }
}


function full_program_filter_rows_on_room(room) {
    if (room == 'all') {
        return jQuery('.presentation-row');
    } else {
        return jQuery('.presentation-row[room*=' + room + ']');
    }
}


function full_program_filter_rows_on_time(timeslot) {
    if (!timeslot || timeslot == 'all') {
        return jQuery('.presentation-row');
	} else if (timeslot == 'now') {
		// Make a timeslot for now to now + 15 minutes that
		// looks like this: 2025-11-10T14:00:00Z|2025-11-10T15:00:00Z
		var now = new Date();
		var start = new Date(now.getTime());
		var end = new Date(now.getTime() + 15 * 60000);
		var start_str = start.toISOString().substr(0, 19) + 'Z';
		var end_str = end.toISOString().substr(0, 19) + 'Z';
		timeslot = start_str + '|' + end_str;

		select_current_date();

		return jQuery('.presentation-row').filter(function () {
			return row_overlaps_time(jQuery(this), timeslot);
		});
	} else {
		return jQuery('.presentation-row').filter(function() {
			return row_overlaps_time(jQuery(this), timeslot);
		});
    }
}


function minutes_since_midnight(stddt) {
	var dt = new Date(stddt);
	var hrs = dt.getUTCHours();
	var mins = dt.getUTCMinutes();
	return hrs * 60 + mins;
}


function row_overlaps_time(row, filter_timeslot) {
	let test_next_day = false;

	row_start_stddt = row.attr('s_utc');
	row_end_stddt = row.attr('e_utc');
	row_start_time = minutes_since_midnight(row_start_stddt);
	row_end_time = minutes_since_midnight(row_end_stddt);
	if (row_end_time < row_start_time) {
		// crosses midnight
		row_end_time += 24 * 60;
		test_next_day = true;
	}
	filter_start_time = minutes_since_midnight(filter_timeslot.substr(0, 20));
	filter_end_time = minutes_since_midnight(filter_timeslot.substr(21, 20));

	// Check for all possible intersections: overlapping, contained, or containing
	let ans = (row_start_time < filter_end_time && row_end_time > filter_start_time);
	if (!ans && test_next_day) {
		// try adding 24 hours to filter times
		filter_start_time += 24 * 60;
		filter_end_time += 24 * 60;
		ans = (row_start_time < filter_end_time && row_end_time > filter_start_time);
	}
	return ans;
}


function full_program_filter_event_handler() {
	// If I call full_program_filter_on_selectors directly from the event then the container gets set as an event.
	full_program_filter_on_selectors();
}


function get_rows_for_filter(filter, filter_func) {
	var rows = jQuery([]);
	var selected;

	// is the filter a select list or a checkbox list?
	if (filter.get(0).nodeName.toLowerCase() == 'select') {
		// If the filter is a select list then we need to get all the selected options.
		selected = filter.find('option:selected');
		// make selected a list of values
	} else {
		// if the filter is a checkbox list then we need to get all the checked boxes.
		// selected = filter.find(':checked');
		var name = filter.first().attr("name")
		selected = jQuery("input[name='" + name + "']:checked")
	}

	var values = [];
	selected.each(function (i) { values[i] = jQuery(this).val() }) || ['']
	selected = values;

	if (selected.length > 0) {
		jQuery(selected).each(function () {
			jQuery.merge(rows, filter_func(this));
		})
	} else if (!filter.hasClass('hides-selected')) {
		rows = filter_func('all');
	}
	return rows;
}


function full_program_filter_on_selectors(container) {

	var show_rows = jQuery('.presentation-row, tr.slots-slidedown');
	var hide_rows = jQuery('.presentation-row, tr.slots-slidedown');
	var hide_any = false;

	selector_filter_map = {
		'[name=etype_filt]': full_program_filter_rows_on_etype,
		'[name^=ptrack_filt]': full_program_filter_rows_on_ptrack,
		'[name=room_filt]': full_program_filter_rows_on_room,
		'[name=time_filt]': full_program_filter_rows_on_time,
	}

	for (const [selector, filter_func] of Object.entries(selector_filter_map)) {
		for (const el of jQuery(selector)) {
			input_ob = jQuery(el);
			input_name = input_ob.attr('name');
			full_ob = jQuery('[name=' + input_name + ']');
			let new_rows = get_rows_for_filter(full_ob, filter_func);
			if (full_ob.hasClass('hides-selected')) {
				if (new_rows.length > 0) {
					hide_any = true;
					hide_rows = find_intersection(hide_rows, new_rows);
				}
			} else {
				show_rows = find_intersection(show_rows, new_rows);
			}
		}
	}

	if (container == undefined) {
	    jQuery('.presentation-row').hide().addClass('filtered');
		// Just collapse all the presentation contents.
		jQuery('tr.slots-slidedown').hide().addClass('filtered');
	} else {
		jQuery(container).find('.presentation-row').hide().addClass('filtered');
		// Just collapse all the presentation contents.
		jQuery(container).find('tr.slots-slidedown').hide().addClass('filtered');
	}

	show_rows.filter(is_not_wrong_date).show().removeClass('filtered');
	if (hide_any) {
		hide_rows.hide().addClass('filtered');
	}

    // Clean up:
    hide_empty_tables(); // This needs more work
    fix_even_odd();
    show_hide_empty_msg();
}


function is_not_wrong_date(i, el) {
	let ans = (!jQuery(el).hasClass('wrong-date'));
	return ans;
}

function is_full_program_page() {
	if (
		(typeof is_agenda_page == 'undefined' || !is_agenda_page) &&
		(typeof is_happening_now_page == 'undefined' || !is_happening_now_page)
	) {
		return jQuery('.linklings-wp-plugin-contents.program').length > 0;
	}
	return false;
}


function full_program_show_filters() {
	if (
		// (typeof is_agenda_page == 'undefined' || !is_agenda_page) &&
		// (typeof is_happening_now_page == 'undefined' || !is_happening_now_page)
		is_full_program_page()
	) {
		jQuery('div.filters').show();

		if (STICKY_FILTER_BAR_TYPE === "top") {
			filters_user_shown = false;
			filter_display = jQuery(".filter_display");
			filters = jQuery(".filters");
			filters_tab = jQuery(".filters_tab");
			filters_box = jQuery(".filters_box");
			onscreen = true;

			filter_display_top = filter_display.offset().top;
			filter_display_height = filter_display.outerHeight();

			jQuery(window).on("scroll resize", function() {
				update_top_sticking_filters();
			});

			filters_tab.on("click", function() {
				toggle_filters_user_shown();
				update_top_sticking_filters();
			});
		}

		update_filter_display();
	}
}


function full_program_toggle_session_contents(psid) {

	var target_row = jQuery('.slots-slidedown.' + psid);

	if (target_row.is(":visible")) {
		// target_row.find('.session-display>div').slideUp('slow', function() {
		target_row.find('.session-display>div').slideUp('fast', function() {
			target_row.hide();
		});
	} else {
		// This causes a pause before the slidedown
		// target_row.show(function() {
		// 	target_row.find('.session-display>div').slideDown('slow');
		// });
		target_row.show();
		target_row.find('.session-display>div').slideDown('fast');
	}

}


function div(text_contents, Class) {
	// var ans = jQuery('<div>' + contents + '</div>').addClass(Class);
	var ans = jQuery('<div>').addClass(Class);
	ans.text(text_contents);
	return ans;
}


function make_countdown_div(target) {

	target = jQuery(target);

	let target_date = target.attr('target_dt');
	// var show_seconds = target.attr('show_seconds');
	let show_seconds = 1;
	let reload = target.attr('reload');
	let hide_when_done = target.attr('hide_when_done');

	let countDownDate = new Date(target_date).getTime();

	let old_url = window.location.toString();
	let new_url = old_url;
	let target_url = target.attr('target_url');
	if (target_url) {
		new_url = target_url;
		reload = true;
	}

	// reload anywhere in the last 45 seconds to spread out server hits.
	let reload_slush = getRandomInt(45) * 1000;
	// let reload_slush = 0;

	let interval_;

	function show_distance_(distance, on_finished) {

		// we don't want to show negative times
		let days = 0;
		let hours = 0;
		let minutes = 0;
		let seconds = 0;

		// If the count down is finished, write some text
		if (distance < reload_slush) {
			if (reload != '0') {
				// This should only happen once, the timer won't be there after the reload.
				clearInterval(interval_);
				// on_finished();
				if (distance >= 0) {
					on_finished();
				} else if (hide_when_done) {
					target.hide();
				}
			} else if (hide_when_done && distance <= 0) {
				clearInterval(interval_);
				target.hide();
			}
		} else {
			// Time calculations for days, hours, minutes and seconds
			days = Math.floor(distance / (1000 * 60 * 60 * 24));
			hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
			minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
			seconds = Math.floor((distance % (1000 * 60)) / 1000);
		}

		minutes = String(minutes).padStart(2, '0');
		seconds = String(seconds).padStart(2, '0');
		let padded_hours = hours;
		if (days) {
			padded_hours = String(hours).padStart(2, '0');
		}

		if (target.attr('setup') != 'yes') {
			target.empty();
			target.attr('setup', 'yes');
			if (days > 0) {
				target.append(
					div(
						'',
						'countdown-days'
					).append(div(days, 'days-count')).append(div('days', 'days-label'))
				)
				target.append(div(':', 'divider'))
			}
			target.append(
				div(
					'',
					'countdown-hours'
				).append(div(padded_hours, 'hours-count')).append(div('hours', 'hours-label'))
			)
			target.append(div(':', 'divider'))
			target.append(
				div(
					'',
					'countdown-minutes'
				).append(div(minutes, 'minutes-count')).append(div('minutes', 'minutes-label'))
			)
			if (show_seconds != '0') {
				target.append(div(':', 'divider').hide())
				target.append(
					div(
						'',
						'countdown-seconds'
					).hide().append(div(seconds, 'seconds-count')).append(div('seconds', 'seconds-label'))
				)
				if (!days && !hours && minutes < 2) {
					jQuery('div.countdown-seconds').css('display', 'inline-block');
					jQuery('div.divider').css('display', 'inline-block');
				}
			}
		} else {
			target.find('.days-count').text(days);
			target.find('.hours-count').text(padded_hours);
			target.find('.minutes-count').text(minutes);
			target.find('.seconds-count').text(seconds);

			if (!days && !hours && minutes < 2) {
				target.find('div.countdown-seconds').show().css('display', 'inline-block');
				target.find('div.divider').show().css('display', 'inline-block');
			}

		}
	}

	let override_str = getQueryVariable('dt_override');
	if (override_str) {
		// This is the testing version, just adds a second
		// every second interval, reloads the page with the
		// target datetime in the url if reload.
		let override_pass = getQueryVariable('pass');
		let now = new Date(override_str).getTime();
		let on_finished = function() {
			// let old_url = window.location.toString();
			// let new_url = old_url.replace(override_str, target_date);
			new_url = setQueryVariable(new_url, 'dt_override', target_date);
			new_url = setQueryVariable(new_url, 'pass', override_pass);
			window.location.replace(new_url);
		}
		let interval_ = setInterval(function () {
			now = now + 1000;
			// Find the distance between now and the count down date
			let distance = countDownDate - now;
			show_distance_(distance, on_finished);

		}, 1000);

	} else {
		// Update the count down every 1 second
		let interval_ = setInterval(function () {

			// Get today's date and time
			let now = new Date().getTime();

			// Find the distance between now and the count down date
			let distance = countDownDate - now;

			// window.location.reload needs window context as this
			// let on_finished = window.location.reload.bind(window.location);
			// let on_finished = window.location.reload.bind(new_url);
			let on_finished = function() {
				window.location.replace(new_url);
			}
			show_distance_(distance, on_finished);

		}, 1000);
	}

}


function start_countdowns() {
	jQuery('.ll_countdown').each(function() {
		make_countdown_div(jQuery(this));
	});
}


function ____________VIMEO_AND_SLIDO________() { }


function get_slido_url(container) {

	if (!container) {
		container = document;
	}
	var slido_span = jQuery('.slido_url:first');
	var slido_url = jQuery(slido_span).attr('url');
	return slido_url
}

function load_slido(slido_frame, slido_url) {
	if (Boolean(slido_url)) {

		// Add the qna token to the slido/qna url if it WP set it.
		// The qna check is mean to match qna.live, staging.qna.live, and qna.sc23.conference-program.com

		// if (WP_LLVP_AGENDA_SYNC_USER.qnaToken && slido_url.indexOf('qna.') != -1) {
		// 	slido_url = setParamsOnURL(slido_url, {
		// 		't': WP_LLVP_AGENDA_SYNC_USER.qnaToken
		// 	});
		// }

		slido_frame.src = slido_url;
	}
}

function get_video_resize_func(container) {

	// This returns a function that can resize and show
	// the vimeo video within <container>.

	let vimeo_frame = jQuery(container).find('.main_video')[0];
	let slido_frame = jQuery(container).find('.slido_frame')[0];
	let wrapper = jQuery(container).find('.ll_vimeo_video_wrapper')[0];

	let slido_url = get_slido_url(container);

	let ans = function () {
		var width = wrapper.clientWidth;
		var disp_under = width < 600;
		if (Boolean(slido_url) && !disp_under) {
			width = 2 * width / 3
		}
		var height = (width * 360 / 640);

		wrapper.style.height = height + 'px';
		vimeo_frame.style.height = height + 'px';
		vimeo_frame.style.width = width + 'px';
		if (Boolean(slido_url)) {
			slido_frame.style.height = height + 'px';
			slido_frame.style.width = (width / 2) + 'px';
			slido_frame.style.top = '0px';
			if (disp_under) {
				slido_frame.style.display = 'block';
				slido_frame.style.top = height + 'px';
				slido_frame.style.width = width + 'px';
				slido_frame.style.height = (height * 3 / 2) + 'px';
				// wrapper.style.height = (height * 2) + 'px';
				wrapper.style.height = (height * 2.5) + 'px';
			}
		} else {
			slido_frame.style.height = '0px';
			slido_frame.style.width = '0px';
		}
	};

	return ans
}


function ____________UTILITIES________() { }


function launchQnaModal(url, scrollToOption, launchedViaPopoutButton=false) {
    const dialog = document.createElement('dialog');
    // FIXME: Update this class name and in styling
    dialog.className = 'chat_modal'; // Keeping the colorbox_chat_link class for now to make sure the original styles are applied

    const iframe = document.createElement('iframe');

    // If scrollToOption is provided, append it to the URL
    if (scrollToOption) {
        const urlObj = new URL(url);
        urlObj.searchParams.append('scroll_to_opt', scrollToOption);
        url = urlObj.toString();
    }

    iframe.src = url;
    iframe.style.width = window.innerWidth * 0.9 + 'px';
    iframe.style.maxWidth = '600px';
    iframe.style.height = window.innerHeight * 0.9 + 'px';
    iframe.style.border = 'none';
    iframe.style.paddingTop = '0px';
    iframe.style.margin = '0px';

    // Add an 'hide_popout_button' class to the iframe element
    if (launchedViaPopoutButton) {
        iframe.className = 'hide-popout-button';
    }

    const close_button = document.createElement('button');
    close_button.className = 'chat_modal_close_button';
    close_button.style.position = 'absolute';
    close_button.style.top = '5px';
    close_button.style.right = '5px';
    close_button.style.padding = '0px';
    close_button.style.width = '40px';
    close_button.style.height = '40px';
    close_button.style.background = 'gray';
    close_button.style.border = 'none';


    const x_icon = document.createElement('i');
    x_icon.className = 'fa-solid fa-x';
    x_icon.style.padding = '0px';
    x_icon.style.margin = '0px';
    x_icon.style.fontSize = '12px';
    close_button.appendChild(x_icon);



    const dialog_content = document.createElement('div');
    dialog_content.appendChild(iframe);
    dialog_content.appendChild(close_button);

    dialog.appendChild(dialog_content);

    document.body.appendChild(dialog);

    // Behavior: escape key closes the modal
    dialog.addEventListener('keypress', event => {
        if (event.key === 'Escape') {
            dialog.close();
        }
    });

    // Behavior: clicking the close button closes the modal
    close_button.addEventListener('click', () => {
        dialog.close();
    });

    dialog.showModal();
}

function loggingDecorator(wrapped) {
	return function () {
		console.log(wrapped.name, arguments);
		const result = wrapped.apply(this, arguments);
		return result;
	}
}

function tryPollModalAutoLaunch() {
    try {
        // Get current URL and parameters
        const currentUrl = window.location.href;
        const url = new URL(currentUrl);
        const urlParams = url.searchParams;

        const showPoll = urlParams.get('showPoll');
        // FIXME: Rename scrollTopOpt to scrollToOption
        // Mapping this to scroll_to_opt in the button click URL params
        const scrollToOption = urlParams.get('scrollTopOpt');

        if (showPoll && (showPoll == 1 || showPoll.toLowerCase() == 'true')) {
            // Get the poll launch anchor link / button
            const pollLink = document.querySelector('.poll-modal-launcher-button-anchor');
            if (pollLink) {
                if (scrollToOption) {
                    pollLink.setAttribute('data-qna-scroll-to-option', scrollToOption);
                }

                // Simulate a click on the link to launch the modal
                pollLink.click();
                pollLink.setAttribute('data-qna-scroll-to-option', ''); // Clean up the attribute

                // Only attempt URL cleanup if NOT Firefox
                // For some reason, Firefox has issues with URL manipulation that result in an infinite page load loop
                if (!/Firefox/i.test(navigator.userAgent)) {
                    try {
                        // Clean up URL parameters
                        // FIXME: Rename scrollTopOpt to scrollToOption
                        if (urlParams.has('showPoll') || urlParams.has('scrollTopOpt')) {
                            urlParams.delete('showPoll');
                            urlParams.delete('scrollTopOpt');

                            // Build new URL preserving other parameters and hash
                            const newUrl = url.pathname +
                                         (urlParams.toString() ? '?' + urlParams.toString() : '') +
                                         (url.hash || '');

                            window.history.replaceState({}, '', newUrl);
                        }
                    } catch (urlError) {
                        console.error('tryPollModalAutoLaunch::Error cleaning URL:', urlError);
                    }
                } else {
                    console.log('tryPollModalAutoLaunch::Skipping URL cleanup in Firefox');
                }
            }
        }
    } catch (error) {
        console.error('tryPollModalAutoLaunch::Error:', error);
    }
}


/**
 * Sets URL parameters on an existing URL.
 *
 * This is a helper function for setting qna user tokens.
 *
 * @param {string} url - The URL to modify.
 * @param {Object} params - A dictionary of URL parameters to append or overwrite.
 */
function setParamsOnURL(url, params) {
	const new_url = new URL(url);
	const urlParams = new URLSearchParams(params);
	urlParams.forEach((value, key) => {
		new_url.searchParams.set(key, value);
	});
	return new_url.toString();
}


function update_goback_url() {
  // Save some breadcrumbs to help with going back to the correct page from a
  // mapplic page.
	if (jQuery('mapplic-map').length === 0) {
		let new_url = window.location.toString();
    // option 1 (deprecated): save the last non-mapplic url.
		sessionStorage.setItem('goback_url', new_url);
		// option 2: save the history index of the last non-mapplic page.
		// (this is better since we can "pop" back the history state)
		sessionStorage.setItem('goback_index', window.history.length);
	}
}


function goback() {
	// If we're not on a mapplic-map page, just go back.
	if (jQuery('mapplic-map').length === 0) {
		window.history.back();
		return;
	}

	// If we are on a mapplic-page, we want to go back to the last non-mapplic page.
	// mapplic adds to the history stack with JS every time a new room is clicked on,
	// and we don't want to force the user have click back through all those rooms.

	let goback_index = sessionStorage.getItem('goback_index');
	let goback_url = sessionStorage.getItem('goback_url');

	// If there is a goback_index in localStorage, use it.
	if (goback_index) {
		sessionStorage.removeItem('goback_index');
		let delta = window.history.length - goback_index;
		window.history.go(-delta);

	// If there is a goback_url in localStorage, use it.
  } else if (goback_url) {
		sessionStorage.removeItem('goback_url');
		window.location.href = goback_url;

	// Otherwise, just go back one page.
	} else {
		window.history.back();
	}
}

if (false) {
	full_program_filter_rows_on_ptrack = loggingDecorator(full_program_filter_rows_on_ptrack);
	setup_timezone_changes = loggingDecorator(setup_timezone_changes);
	changeDateTime = loggingDecorator(changeDateTime);
	start_countdowns = loggingDecorator(start_countdowns);
}
