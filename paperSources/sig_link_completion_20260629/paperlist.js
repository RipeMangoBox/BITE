function pcPaperlistIsTextEntryHotkeyTarget(event) {
    const rawTarget = event && event.target;
    const target = rawTarget && rawTarget.nodeType === 1 ? rawTarget : rawTarget && rawTarget.parentElement;
    if (!target) return false;
    if (target.isContentEditable) return true;
    const tag = (target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'textarea' || tag === 'select') return true;
    return !!(target.closest && target.closest('input, textarea, select, [contenteditable="true"], [contenteditable="plaintext-only"], [role="textbox"]'));
}

// https://observablehq.com/@d3/stacked-bar-chart
function ZoomableBarChart(data, {
    width = 600,
    height = 400,
    marginTop = 50,
    marginRight = 40,
    marginBottom = 40,
    marginLeft = 40,
    labelTitleSize = 15, // label font size for axis
    xLabel = "X →",
    yLabel = "↑ Y",
    show_frequency = false,
    show_labels = true,
} = {}) {

    // Create the horizontal scale and its axis generator.
    const x = d3.scaleBand()
        .domain(d3.sort(data, d => -d.frequency).map(d => d.letter))
        .range([marginLeft, width - marginRight])
        .padding(0.1);

    const xAxis = d3.axisBottom(x)
        .tickSizeOuter(0)
        .tickFormat(d => {
            const item = data.find(item => item.letter === d);
            return `${item.letter}`;
        });

    const xAxis_idx = d3.axisBottom(x)
        .tickSizeOuter(0)
        .tickFormat((d, i) => {
            const item = data.find(item => item.letter === d);
            return i + 1;
        });

    // Create the vertical scale.
    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.frequency)]).nice()
        .range([height - marginBottom, marginTop]);

    // Create the SVG container and call the zoom behavior.
    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("width", width)
        .attr("height", height)
        .attr("style", "max-width: 100%; height: auto;")
        .call(zoom);

    // Append the bars.
    svg.append("g")
        .attr("class", "bars")
        .attr("fill", "steelblue")
        .selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", d => x(d.letter))
        .attr("y", d => y(d.frequency))
        .attr("height", d => y(0) - y(d.frequency))
        .attr("width", x.bandwidth())
        .append("title")
        .text(d => `${d.letter}\n${d.frequency} papers accepted`);

    // Append the frequency labels above the bars.
    if (show_frequency) {
        svg.append("g")
            .attr("class", "frequency-labels")
            .selectAll("text")
            .data(data)
            .join("text")
            .attr("x", d => x(d.letter) + x.bandwidth() / 2)
            .attr("y", d => y(d.frequency) - 5) // Positioning the label above the bar
            .attr("text-anchor", "middle")
            .attr('font-size', '10px')
            .attr("fill", "black")
            .attr("opacity", show_frequency ? 1 : 0)
            .text(d => d.frequency);
    }

    // Append the x axes.
    if (show_labels) {
        svg.append("g")
            .attr("class", "x-axis")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .call(xAxis)
            .call(g => { // rotate text labels for each bar
                g.selectAll("text")
                    .attr("dx", 5)
                    .attr("dy", -6)
                    .attr("transform", "rotate(-90)")
                    .attr("fill", "black")
                    .attr('font-size', '10px')
                    // .attr("opacity", show_labels ? 1 : 0)
                    .style("text-anchor", "start")
            });
    }

    // Append the x index axis
    svg.append("g")
        .attr("class", "x-axis-index")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(xAxis_idx)
        .call(g => { // rotate text labels for each bar
            g.selectAll("text")
                .attr("dx", -8)
                .attr("dy", -6)
                .attr("transform", "rotate(-90)")
                .style("text-anchor", "end")
        })
        .call(g => g.append("text") // x-axis label
            .attr("x", width - marginRight)
            .attr("y", 35)
            .attr("fill", "currentColor")
            .attr("text-anchor", "end")
            .attr("font-size", labelTitleSize)
            .text(xLabel));

    // Append the y axes.
    svg.append("g")
        .attr("class", "y-axis")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y))
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").clone() // y-axis grid lines
            .attr("x2", width - marginLeft - marginRight)
            .attr("stroke-opacity", 0.1))
        .call(g => g.append("text")
            .attr("x", -marginLeft)
            .attr("y", marginTop - 30)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .attr("font-size", labelTitleSize)
            .text(yLabel));

    return svg.node();

    function zoom(svg) {
        const extent = [[marginLeft, marginTop], [width - marginRight, height - marginTop]];

        svg.call(d3.zoom()
            .scaleExtent([1, 8])
            .translateExtent(extent)
            .extent(extent)
            .on("zoom", zoomed));

        function zoomed(event) {
            x.range([marginLeft, width - marginRight].map(d => event.transform.applyX(d)));
            svg.selectAll(".bars rect").attr("x", d => x(d.letter)).attr("width", x.bandwidth());
            svg.selectAll(".frequency-labels text").attr("x", d => x(d.letter) + x.bandwidth() / 2);
            svg.selectAll(".letter-labels text").attr("x", d => x(d.letter) + x.bandwidth() / 2);
            svg.selectAll(".x-axis").call(xAxis);
            svg.selectAll(".x-axis-index").call(xAxis_idx);
            const newFontSize = Math.max(10, Math.min(20, x.bandwidth() * 0.5));
            svg.selectAll(".x-axis text").attr('font-size', `${newFontSize}px`);
        }
    }
}

function ZoomableStackedBarChart(data, {
    width = 600,
    height = 400,
    marginTop = 50,
    marginRight = 40,
    marginBottom = 40,
    marginLeft = 40,
    labelTitleSize = 15,
    xLabel = "X →",
    yLabel = "↑ Y",
    show_frequency = false,
    show_labels = true,
    keys = [],
    num_bars = 100,
    // New options for animation
    enableAnimation = true,
    animationDuration = 500,
} = {}) {

    let hiddenKeys = new Set();

    const color = d3.scaleOrdinal()
        .domain(keys)
        .range(d3.schemeCategory10);

    let x = d3.scaleBand()
        .domain(data.map(d => d.letter))
        .range([marginLeft, width - marginRight])
        .padding(0.1);

    let y = d3.scaleLinear()
        .domain([0, d3.max(data, d => {
            return keys.reduce((acc, k) => acc + (d[k] || 0), 0);
        })]).nice()
        .range([height - marginBottom, marginTop]);

    let stack = d3.stack()
        .keys(keys)
        .order(d3.stackOrderNone)
        .offset(d3.stackOffsetNone);

    const svg = d3.create("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("width", width)
        .attr("height", height)
        .style("max-width", "100%")
        .call(zoom);

    const barsContainer = svg.append("g")
        .attr("class", "bars-container");

    const labelsContainer = svg.append("g")
        .attr("class", "labels-container");

    svg.append("g")
        .attr("class", "y-axis")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y).tickSizeOuter(0))
        .call(g => g.select(".domain").remove())
        .call(g => g.selectAll(".tick line").clone()
            .attr("x2", width - marginLeft - marginRight)
            .attr("stroke-opacity", 0.1))
        .call(g => g.append("text")
            .attr("x", -marginLeft)
            .attr("y", marginTop - 30)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .attr("font-size", labelTitleSize)
            .text(yLabel));

    svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height - marginBottom})`);

    svg.append("g")
        .attr("class", "x-axis-index")
        .attr("transform", `translate(0,${height - marginBottom})`);

    function updateChart() {
        // Conditionally define the transition
        const t = enableAnimation
            ? svg.transition().duration(animationDuration)
            : svg.transition().duration(0);

        // 1) Filter out hidden keys
        let activeKeys = keys.filter(k => !hiddenKeys.has(k));

        // 2) Re-sort data by sum of active keys
        data.sort((a, b) => {
            const sumA = activeKeys.reduce((acc, k) => acc + (a[k] || 0), 0);
            const sumB = activeKeys.reduce((acc, k) => acc + (b[k] || 0), 0);
            count_order = sumB - sumA;
            alphabet_order = a.letter.localeCompare(b.letter);

            // Sort descending by sum, then ascending by letter if sums are equal
            return count_order || alphabet_order;
        });

        // 3) Slice top N bars
        const topData = data.slice(0, num_bars);

        // 4) Recompute stacked data
        let newStack = d3.stack().keys(activeKeys)(topData);

        // 5) Update domains
        x.domain(topData.map(d => d.letter));
        let maxY = d3.max(newStack, layer => d3.max(layer, d => d[1]));
        y.domain([0, maxY]).nice();

        // 6) Update x-axis
        const xAxis = d3.axisBottom(x).tickSizeOuter(0).tickFormat(d => d);
        if (show_labels) {
            svg.select(".x-axis")
                .transition(t)
                .call(xAxis)
                .selection()
                .selectAll("text")
                    .attr("dx", 5)
                    .attr("dy", -6)
                    .attr("transform", "rotate(-90)")
                    .attr("fill", "black")
                    .attr('font-size', '10px')
                    .style("text-anchor", "start");
        } else {
            // If show_labels is false, remove text or empty the tickFormat
            svg.select(".x-axis")
                .transition(t)
                .call(xAxis.tickFormat(() => ""));
        }

        // 7) Update x-axis index
        const xAxis_idx = d3.axisBottom(x).tickSizeOuter(0).tickFormat((d, i) => i + 1);
        svg.select(".x-axis-index")
            .transition(t)
            .call(xAxis_idx)
            .selection()
            .selectAll(".tick text")
                .attr("dx", -8)
                .attr("dy", -6)
                .attr("transform", "rotate(-90)")
                .style("text-anchor", "end");

        // Add label for x-axis
        svg.select(".x-axis-index")
            .selectAll("text.x-axis-label").data([null])
            .join("text")
            .attr("class", "x-axis-label")
            .attr("x", width - marginRight)
            .attr("y", 35)
            .attr("fill", "currentColor")
            .attr("text-anchor", "end")
            .attr("font-size", labelTitleSize)
            .text(xLabel);

        // 8) Update y-axis
        const yAxis = d3.axisLeft(y).tickSizeOuter(0);
        svg.select(".y-axis")
            .transition(t)
            .call(yAxis);

        // 9) Join + Update the stacked bars
        let seriesBars = barsContainer
            .selectAll("g.series")
            .data(newStack, d => d.key);

        seriesBars.exit().remove();

        let seriesBarsEnter = seriesBars.enter()
            .append("g")
            .attr("class", "series")
            .attr("fill", d => color(d.key));

        seriesBars = seriesBarsEnter.merge(seriesBars);

        // Add the 'key' property to each stacked segment for tooltips
        newStack.forEach(series => {
            series.forEach(d => {
                d.key = series.key;
            });
        });

        let rects = seriesBars.selectAll("rect")
            .data(d => d, d => d.data.letter);

        // ENTER: set bars to zero height
        rects.enter()
            .append("rect")
            .attr("x", d => x(d.data.letter))
            .attr("y", y(0))
            .attr("height", 0)
            .attr("width", x.bandwidth())
            // set up tooltip <title>
            .call(sel => sel.append("title"))
            .merge(rects)
            // UPDATE: transition to final positions
            .transition(t)
            .attr("x", d => x(d.data.letter))
            .attr("y", d => y(d[1]))
            .attr("height", d => y(d[0]) - y(d[1]))
            .attr("width", x.bandwidth());

        // Update tooltip text (no transition needed)
        seriesBars.selectAll("rect title")
            .text(d => {
                let key = d.key;
                let value = d[1] - d[0];
                let letter = d.data.letter;
                return `${letter}\n${key}: ${value}`;
            });

        // EXIT: transition bars back to zero height
        rects.exit()
            .transition(t)
            .attr("y", y(0))
            .attr("height", 0)
            .remove();

        // 10) Show frequency labels if enabled
        if (show_frequency) {
            let seriesLabels = labelsContainer
                .selectAll("g.seriesLabels")
                .data(newStack, d => d.key);

            seriesLabels.exit().remove();

            let seriesLabelsEnter = seriesLabels.enter()
                .append("g")
                .attr("class", "seriesLabels");

            seriesLabels = seriesLabelsEnter.merge(seriesLabels);

            let texts = seriesLabels.selectAll("text.frequency-label")
                .data(d => d, d => d.data.letter);

            texts.enter()
                .append("text")
                .attr("class", "frequency-label")
                .attr("x", d => x(d.data.letter) + (show_labels ? 0.75 : 0.5) * x.bandwidth())
                .attr("y", y(0)) // start at bottom
                .attr("text-anchor", "middle")
                .attr("font-size", "10px")
                .attr("fill", "black")
                .merge(texts)
                .transition(t)
                .attr("x", d => x(d.data.letter) + (show_labels ? 0.75 : 0.5) * x.bandwidth())
                .attr("y", d => y(d[1]) - 5)
                .text(d => `${d[1]}`);

            texts.exit()
                .transition(t)
                .attr("y", y(0))
                .remove();

        } else {
            labelsContainer.selectAll("g.seriesLabels").remove();
        }

        // Fade legend items for hiddenKeys
        legend.selectAll("g.legend-item")
            .attr("opacity", (d, i, nodes) => {
                const keyName = d3.select(nodes[i]).select("text").text();
                return hiddenKeys.has(keyName) ? 0.3 : 1.0;
            });
    }

    // Legend
    const legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${width - marginRight + 10},${0})`);

    const legendTitle = legend.append("text")
        .attr("class", "legend-title")
        .attr("y", -30 + marginTop)
        .attr("font-size", 10)
        .attr("text-anchor", "end");

    legendTitle.append("tspan")
        .attr("x", -marginRight + 15)
        .attr("dy", "1em")
        .text("Ctrl+Click to isolate");

    legendTitle.append("tspan")
        .attr("x", -marginRight + 15)
        .attr("dy", "1.2em")
        .text("Click to toggle");

    keys.forEach((key, i) => {
        const legendRow = legend.append("g")
            .attr("class", "legend-item")
            .attr("transform", `translate(-${marginRight}, ${i * 20 + marginTop})`)
            .attr("font-family", "sans-serif")
            .attr("font-size", 12)
            .style("cursor", "pointer")
            .on("click", (event) => legendClicked(event, key));

        legendRow.append("rect")
            .attr("width", 15)
            .attr("height", 15)
            .attr("fill", color(key));

        legendRow.append("text")
            .attr("x", -6)
            .attr("y", 12)
            .attr("text-anchor", "end")
            .text(key);
    });

    // Some text notes
    const notes = [
        'Notes:',
        'Feel free to use/download charts; credit to papercopilot is appreciated.',
        'The clickable legend re-sorts only the top 200 bars summarized from the whole dataset. For more complete data, please see the raw GitHub dataset.',
        'Press [S] or click gear to toggle settings.',
    ];
    for (let i = 0; i < notes.length; i++) {
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", marginTop + i * 15)
            .attr("fill", "currentColor")
            .attr("text-anchor", "middle")
            .attr("font-size", 12)
            .text(notes[i]);
    }

    updateChart();

    function zoom(svg) {
        const extent = [[marginLeft, marginTop], [width - marginRight, height - marginTop]];
        svg.call(d3.zoom()
            .scaleExtent([1, 8])
            .translateExtent(extent)
            .extent(extent)
            .on("zoom", zoomed));

        function zoomed(event) {
            x.range([marginLeft, width - marginRight].map(d => event.transform.applyX(d)));
            barsContainer.selectAll("rect")
                .attr("x", d => x(d.data.letter))
                .attr("width", x.bandwidth());
            svg.select(".x-axis").call(d3.axisBottom(x));
            svg.select(".x-axis-index").call(d3.axisBottom(x).tickFormat((d, i) => i + 1));

            let newFontSize = Math.max(10, Math.min(18, x.bandwidth() * 0.5));
            svg.selectAll(".x-axis text").attr('font-size', `${newFontSize}px`);

            labelsContainer.selectAll("text.frequency-label")
                .attr("x", d => x(d.data.letter) + (show_labels ? 0.75 : 0.5) * x.bandwidth());
        }
    }

    function legendClicked(event, clickedKey) {
        if (event.ctrlKey || event.metaKey) {
            const onlyClickedKeyVisible = (
                hiddenKeys.size === keys.length - 1 &&
                !hiddenKeys.has(clickedKey)
            );
            if (onlyClickedKeyVisible) {
                hiddenKeys.clear();
            } else {
                hiddenKeys = new Set(keys.filter(k => k !== clickedKey));
            }
        } else {
            if (hiddenKeys.has(clickedKey)) {
                hiddenKeys.delete(clickedKey);
            } else {
                hiddenKeys.add(clickedKey);
            }
        }
        updateChart();
    }

    return svg;
}


function pcPaperlistLegacyCreateGearButton(svg, options = {}) {
    // Default configuration options
    const config = {
        size: 45,                        // Size of the gear button
        x: svg.attr("width") / 2,        // X-position (centered by default)
        y: 8,                           // Y-position (top by default)
        fillColor: "#00000000",               // Fill color of the gear
        strokeColor: "#333",             // Stroke color of the gear
        strokeWidth: 2,                  // Stroke width
        tooltipText: "Settings",         // Tooltip text to show on hover
        onClick: () => onclick_btn_setting // Default click event
    };

    // Merge provided options with defaults
    Object.assign(config, options);

    // Define the gear icon path
    const gearIconPath = "M10.4 5.6C10.4 4.84575 10.4 4.46863 10.6343 4.23431C10.8686 4 11.2458 4 12 4C12.7542 4 13.1314 4 13.3657 4.23431C13.6 4.46863 13.6 4.84575 13.6 5.6V6.6319C13.9725 6.74275 14.3287 6.8913 14.6642 7.07314L15.3942 6.34315C15.9275 5.80982 16.1942 5.54315 16.5256 5.54315C16.8569 5.54315 17.1236 5.80982 17.6569 6.34315C18.1903 6.87649 18.4569 7.14315 18.4569 7.47452C18.4569 7.80589 18.1903 8.07256 17.6569 8.60589L16.9269 9.33591C17.1087 9.67142 17.2573 10.0276 17.3681 10.4H18.4C19.1542 10.4 19.5314 10.4 19.7657 10.6343C20 10.8686 20 11.2458 20 12C20 12.7542 20 13.1314 19.7657 13.3657C19.5314 13.6 19.1542 13.6 18.4 13.6H17.3681C17.2573 13.9724 17.1087 14.3286 16.9269 14.6641L17.6569 15.3941C18.1902 15.9275 18.4569 16.1941 18.4569 16.5255C18.4569 16.8569 18.1902 17.1235 17.6569 17.6569C17.1236 18.1902 16.8569 18.4569 16.5255 18.4569C16.1942 18.4569 15.9275 18.1902 15.3942 17.6569L14.6642 16.9269C14.3286 17.1087 13.9724 17.2573 13.6 17.3681V18.4C13.6 19.1542 13.6 19.5314 13.3657 19.7657C13.1314 20 12.7542 20 12 20C11.2458 20 10.8686 20 10.6343 19.7657C10.4 19.5314 10.4 19.1542 10.4 18.4V17.3681C10.0276 17.2573 9.67142 17.1087 9.33591 16.9269L8.60598 17.6569C8.07265 18.1902 7.80598 18.4569 7.47461 18.4569C7.14324 18.4569 6.87657 18.1902 6.34324 17.6569C5.80991 17.1235 5.54324 16.8569 5.54324 16.5255C5.54324 16.1941 5.80991 15.9275 6.34324 15.3941L7.07314 14.6642C6.8913 14.3287 6.74275 13.9725 6.6319 13.6H5.6C4.84575 13.6 4.46863 13.6 4.23431 13.3657C4 13.1314 4 12.7542 4 12C4 11.2458 4 10.8686 4.23431 10.6343C4.46863 10.4 4.84575 10.4 5.6 10.4H6.6319C6.74275 10.0276 6.8913 9.67135 7.07312 9.33581L6.3432 8.60589C5.80987 8.07256 5.5432 7.80589 5.5432 7.47452C5.5432 7.14315 5.80987 6.87648 6.3432 6.34315C6.87654 5.80982 7.1432 5.54315 7.47457 5.54315C7.80594 5.54315 8.07261 5.80982 8.60594 6.34315L9.33588 7.07308C9.6714 6.89128 10.0276 6.74274 10.4 6.6319V5.6Z";

    // Append the gear icon to the SVG and apply configuration
    const gearButton = svg.append("path")
        .attr("d", gearIconPath)
        .attr("transform", `translate(${config.x - config.size / 2}, ${config.y})`)
        .attr("fill", config.fillColor)
        .attr("stroke", config.strokeColor)
        .attr("stroke-width", config.strokeWidth)
        .style("cursor", "pointer")
        .on("click", config.onClick);

    // Tooltip for hover effect
    const tooltip = svg.append("text")
        .attr("x", config.x + config.size / 2 + 10)
        .attr("y", config.y + config.size / 2 - 6)
        .attr("text-anchor", "middle")
        .attr("fill", "#333")
        .attr("font-size", "12px")
        .attr("visibility", "hidden")
        .text(config.tooltipText);

    // Show tooltip on hover
    gearButton
        .on("mouseover", () => {
            tooltip.attr("visibility", "visible");
        })
        .on("mouseout", () => {
            tooltip.attr("visibility", "hidden");
        });

    return gearButton;
}

const PC_PAPERLIST_GEAR_SVG = '<svg class="pc_action_gear" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="flex-shrink:0"><path d="M12 15.5A3.5 3.5 0 018.5 12 3.5 3.5 0 0112 8.5a3.5 3.5 0 013.5 3.5 3.5 3.5 0 01-3.5 3.5m7.43-2.53c.04-.32.07-.64.07-.97 0-.33-.03-.66-.07-1l2.11-1.63c.19-.15.24-.42.12-.64l-2-3.46a.5.5 0 00-.61-.22l-2.49 1c-.52-.39-1.06-.73-1.69-.98l-.37-2.65A.506.506 0 0014 2h-4c-.25 0-.46.18-.5.42l-.37 2.65c-.63.25-1.17.59-1.69.98l-2.49-1a.5.5 0 00-.61.22l-2 3.46c-.13.22-.07.49.12.64L4.57 11c-.04.34-.07.67-.07 1 0 .33.03.65.07.97l-2.11 1.66c-.19.15-.25.42-.12.64l2 3.46c.12.22.39.31.61.22l2.49-1.01c.52.4 1.06.74 1.69.99l.37 2.65c.04.24.25.42.5.42h4c.25 0 .46-.18.5-.42l.37-2.65c.63-.26 1.17-.59 1.69-.99l2.49 1.01a.5.5 0 00.61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.66z"/></svg>';


/***************************************************/
/*                                                 */
/*             Jquery starts from here             */
/*                                                 */
/***************************************************/
jQuery(document).ready(function ($) {
    function pcBootSharedPaperlistChart() {
        if (!window.meta || !meta.xaxis || !Array.isArray(meta.status)) return false;
        if (window.pcPaperlistSharedMounted) return true;
        window.pcPaperlistSharedMounted = true;

    (function mountSharedPaperlistChart() {
        const AXIS_LABELS = {
            authors: 'Names',
            authors_id: 'OpenReview IDs',
            authors_first: 'First Author Names',
            authors_id_first: 'First Author IDs',
            authors_last: 'Last Author Names',
            authors_id_last: 'Last Author IDs',
            affiliations: 'All Affiliations',
            affiliations_unique: 'Unique per Paper',
            affiliations_first: 'First Author Affiliation',
            affiliations_last: 'Last Author Affiliation',
            affiliations_country: 'All Countries',
            affiliations_country_unique: 'Unique per Paper',
            affiliations_country_first: 'First Author Country',
            affiliations_country_last: 'Last Author Country',
            positions: 'All Positions',
            positions_unique: 'Unique per Paper',
            positions_first: 'First Author Position',
            positions_last: 'Last Author Position',
            keywords: 'All Keywords',
            keywords_first: 'First Keyword',
        };
        const AXIS_ORDER = Object.keys(AXIS_LABELS);
        const AXIS_GROUP_ORDER = ['Authors', 'Affiliations', 'Countries', 'Positions', 'Keywords', 'Other'];
        const AXIS_ID_EQUIVALENTS = {
            authors_id: 'authors',
            authors_id_first: 'authors_first',
            authors_id_last: 'authors_last',
        };
        const STATUS_VIEWS = [
            { value: 'Submitted', label: 'All Tiers', desc: 'Every decision tier' },
            { value: 'Accepted', label: 'Accepted', desc: 'Accepted tiers' },
            { value: 'Rejected', label: 'Rejected', desc: 'Rejected and withdrawn tiers' },
        ];
        const CHART_TYPES = [
            { value: 'Treemap', label: 'Treemap', group: 'Overview' },
            { value: 'Flow', label: 'Relationship Flow', group: 'Relationships' },
            { value: 'StackedBar', label: 'Stacked Bar', group: 'Bars & Lines' },
            { value: 'GroupedBar', label: 'Grouped Bar', group: 'Bars & Lines' },
            { value: 'OverlaidBar', label: 'Overlaid Bar', group: 'Bars & Lines' },
            { value: 'Line', label: 'Line', group: 'Bars & Lines' },
        ];
        const CHART_GROUP_ORDER = ['Overview', 'Relationships', 'Bars & Lines'];
        const TILE_CHART_TYPES = ['Status pie', 'Status grouped', 'None'];
        const TOP_CAP = 1000;
        const REJECT_RE = /reject|withdraw/i;
        const SINGLE_KEY = 'Count';
        const ajaxInfo = window.ajaxmeta || {};
        const compareCache = new Map();
        const compareFlights = new Map();
        const flowCache = new Map();
        const flowFlights = new Map();
        let compareDataset = null;
        let compareError = '';
        let flowError = '';
        const isRelationshipSurface = ['authorship', 'affiliation', 'countries'].includes(String(ajaxInfo.surface || ''));
        const argsInit = {
            view: isRelationshipSurface ? 'Submitted' : 'Accepted',
            chart: 'Treemap',
            xaxis: '',
            numBars: 100,
            showLabels: true,
            animate: true,
            width: 1400,
            height: window.innerWidth / window.innerHeight > 1.1 ? 600 : 1000,
            downloadFormat: 'png',
            tileChart: 'Status pie',
            comparison: {
                active: false,
                conf: '',
                year: '',
                mode: 'normalized',
                layout: 'split_h',
            },
            line: { show: true, mode: 'cumulative', curve: 'catmull-rom' },
        };
        const args = {
            ...argsInit,
            comparison: { ...argsInit.comparison },
            line: { ...argsInit.line },
        };
        const currentDataset = makeDataset(meta, {
            conf: ajaxInfo.conf,
            year: ajaxInfo.year,
            track: ajaxInfo.track || 'main',
        });

        function esc(text) {
            return String(text == null ? '' : text)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
        }

        function splitConfYear(conference) {
            const match = String(conference || '').match(/^([a-z][a-z0-9_]*?)(\d{4})$/i);
            return match ? { conf: match[1].toLowerCase(), year: Number(match[2]) } : { conf: '', year: '' };
        }

        function makeDataset(metaObj, options = {}) {
            metaObj = metaObj || {};
            const inferred = splitConfYear((metaObj && metaObj.conference && metaObj.conference[0]) || '');
            const conf = String(options.conf || metaObj.conf || inferred.conf || '').toLowerCase();
            const year = Number(options.year || metaObj.year || inferred.year || 0) || '';
            const track = String(options.track || metaObj.track || 'main');
            return {
                meta: metaObj || { status: [], xaxis: {} },
                conf,
                year,
                track,
                label: options.label || metaObj.label || [conf ? conf.toUpperCase() : '', year].filter(Boolean).join(' '),
                parsedCache: new Map(),
            };
        }

        function axisLabel(key) {
            return AXIS_LABELS[key] || String(key || '').replace(/_/g, ' ');
        }

        function axisGroupLabel(key) {
            key = String(key || '');
            if (key.startsWith('authors')) return 'Authors';
            if (key.startsWith('affiliations_country')) return 'Countries';
            if (key.startsWith('affiliations')) return 'Affiliations';
            if (key.startsWith('positions')) return 'Positions';
            if (key.startsWith('keywords')) return 'Keywords';
            return 'Other';
        }

        function axisOptionsHtml() {
            const grouped = new Map();
            availableAxes.forEach(axis => {
                const group = axisGroupLabel(axis);
                if (!grouped.has(group)) grouped.set(group, []);
                grouped.get(group).push(axis);
            });
            const groups = AXIS_GROUP_ORDER
                .concat(Array.from(grouped.keys()).filter(group => !AXIS_GROUP_ORDER.includes(group)))
                .filter((group, idx, arr) => grouped.has(group) && arr.indexOf(group) === idx);
            return groups.map(group => {
                const options = grouped.get(group)
                    .map(axis => `<option value="${esc(axis)}">${esc(axisLabel(axis))}</option>`)
                    .join('');
                return `<optgroup label="${esc(group)}">${options}</optgroup>`;
            }).join('');
        }

        function chartOptionsHtml() {
            const grouped = new Map();
            CHART_TYPES.forEach(chart => {
                const group = chart.group || 'Other';
                if (!grouped.has(group)) grouped.set(group, []);
                grouped.get(group).push(chart);
            });
            const groups = CHART_GROUP_ORDER
                .concat(Array.from(grouped.keys()).filter(group => !CHART_GROUP_ORDER.includes(group)))
                .filter((group, idx, arr) => grouped.has(group) && arr.indexOf(group) === idx);
            return groups.map(group => {
                const options = grouped.get(group)
                    .map(chart => `<option value="${esc(chart.value)}">${esc(chart.label)}</option>`)
                    .join('');
                return `<optgroup label="${esc(group)}">${options}</optgroup>`;
            }).join('');
        }

        function viewLabel(view) {
            const opt = STATUS_VIEWS.find(d => d.value === view);
            return opt ? opt.label : view;
        }

        function metricString(axis, dataset = currentDataset) {
            const arr = dataset && dataset.meta && dataset.meta.xaxis ? dataset.meta.xaxis[axis] : '';
            return Array.isArray(arr) ? String(arr[0] || '') : String(arr || '');
        }

        function parseEntries(axis, dataset = currentDataset) {
            const cache = dataset.parsedCache || (dataset.parsedCache = new Map());
            if (cache.has(axis)) return cache.get(axis);
            const bins = [];
            let summaryOnly = false;
            String(metricString(axis, dataset) || '').split(';').forEach((raw, i) => {
                const entry = raw.trim();
                if (!entry) return;
                const parts = entry.split(':');
                if (parts.length < 2) return;
                let label;
                let totalText;
                let countsText = '';
                if (parts.length === 2) {
                    label = parts[0];
                    totalText = parts[1];
                    summaryOnly = true;
                } else {
                    countsText = parts.pop();
                    totalText = parts.pop();
                    label = parts.join(':');
                }
                label = String(label || '').trim();
                const total = Number.parseInt(totalText, 10) || 0;
                if (!label || total <= 0) return;
                const counts = {};
                if (countsText) {
                    const rawCounts = countsText.split(',').map(v => Number.parseInt(v, 10) || 0);
                    (dataset.meta.status || []).forEach((status, idx) => {
                        counts[status] = rawCounts[idx] || 0;
                    });
                }
                bins.push({ key: `${i}:${label}`, label, total, counts, sourceIndex: i });
            });
            const parsed = { bins, summaryOnly };
            cache.set(axis, parsed);
            return parsed;
        }

        function axisHasData(axis, dataset = currentDataset) {
            return parseEntries(axis, dataset).bins.length > 0;
        }

        function axisIsRedundantId(axis) {
            const equivalent = AXIS_ID_EQUIVALENTS[axis];
            return !!(equivalent
                && Object.prototype.hasOwnProperty.call(currentDataset.meta.xaxis, equivalent)
                && axisHasData(equivalent));
        }

        const availableAxes = AXIS_ORDER
            .filter(axis => Object.prototype.hasOwnProperty.call(currentDataset.meta.xaxis, axis))
            .concat(Object.keys(currentDataset.meta.xaxis).filter(axis => !AXIS_ORDER.includes(axis)))
            .filter(axis => axisHasData(axis) && !axisIsRedundantId(axis));

        if (!availableAxes.length) return;
        args.xaxis = ajaxInfo.default_xaxis && availableAxes.includes(ajaxInfo.default_xaxis)
            ? ajaxInfo.default_xaxis
            : availableAxes[0];

        function statusKeysFor(view, parsed, dataset = currentDataset) {
            if (parsed.summaryOnly) return [SINGLE_KEY];
            let keys;
            if (view === 'Submitted') {
                keys = (dataset.meta.status || []).slice();
            } else if (view === 'Rejected') {
                keys = (dataset.meta.status || []).filter(s => REJECT_RE.test(s));
            } else {
                keys = (dataset.meta.status || []).filter(s => !REJECT_RE.test(s));
            }
            const present = keys.filter(key => parsed.bins.some(d => (Number(d.counts[key]) || 0) > 0));
            if (present.length) return present;
            return keys.length ? keys : [SINGLE_KEY];
        }

        function unionStatusKeys(a, b, datasets = [currentDataset]) {
            const set = new Set([...(a || []), ...(b || [])]);
            if (set.has(SINGLE_KEY)) return [SINGLE_KEY];
            const order = [];
            datasets.forEach(dataset => {
                ((dataset && dataset.meta && dataset.meta.status) || []).forEach(status => {
                    if (!order.includes(status)) order.push(status);
                });
            });
            const ordered = order.filter(status => set.has(status));
            const extra = Array.from(set).filter(status => !order.includes(status));
            return ordered.concat(extra);
        }

        function countFor(entry, status, parsed) {
            if (!entry) return 0;
            if (parsed.summaryOnly || status === SINGLE_KEY) return Number(entry.total) || 0;
            return Number(entry.counts[status]) || 0;
        }

        function totalFor(entry, keys, parsed) {
            return keys.reduce((sum, key) => sum + countFor(entry, key, parsed), 0);
        }

        function sortedEntries(parsed, rankKeys) {
            return parsed.bins
                .map(d => ({ ...d, _sum: totalFor(d, rankKeys, parsed) }))
                .filter(d => d._sum > 0)
                .sort((a, b) => d3.descending(a._sum, b._sum) || d3.ascending(a.label, b.label));
        }

        function rankedEntries(parsed, rankKeys) {
            return sortedEntries(parsed, rankKeys).slice(0, Math.max(1, args.numBars));
        }

        function canonicalEntryRows(currentParsed, currentKeys, compareParsed, compareKeys, zDomain) {
            const rows = new Map();
            const addSide = (side, parsed, keys) => {
                if (!parsed) return;
                sortedEntries(parsed, zDomain).forEach(entry => {
                    const key = String(entry.label || '').toLowerCase();
                    if (!key) return;
                    if (!rows.has(key)) {
                        rows.set(key, { key, label: entry.label, current: null, compare: null, score: 0 });
                    }
                    const row = rows.get(key);
                    row[side] = entry;
                    row.score += totalFor(entry, keys, parsed);
                });
            };
            addSide('current', currentParsed, currentKeys);
            addSide('compare', compareParsed, compareKeys);
            return Array.from(rows.values())
                .filter(row => row.score > 0)
                .sort((a, b) => d3.descending(a.score, b.score) || d3.ascending(a.label, b.label));
        }

        function sideEntries(entries, side) {
            return entries.map(entry => entry[side]).filter(Boolean);
        }

        function axisLimit(axis = args.xaxis) {
            const currentCount = parseEntries(axis, currentDataset).bins.length || 0;
            const compareCount = compareDataset && axisHasData(axis, compareDataset)
                ? parseEntries(axis, compareDataset).bins.length
                : 0;
            return Math.max(1, currentCount, compareCount, args.numBars || 1);
        }

        function topLimit(axis = args.xaxis) {
            return Math.max(1, Math.min(TOP_CAP, axisLimit(axis)));
        }

        function rowsFor(entries, side, selectedKeys, zDomain, parsed) {
            const selected = new Set(selectedKeys);
            return entries.flatMap((entry, i) => zDomain.map(status => ({
                x0: i,
                x1: i + 1,
                status,
                f: selected.has(status) ? countFor(entry[side], status, parsed) : 0,
            })));
        }

        function colorFor(status, zDomain) {
            if (typeof window.pcTierColorMap === 'function') {
                const order = statusOrderForColors(zDomain);
                const map = window.pcTierColorMap(order, zDomain);
                if (map && map[status]) return map[status];
            }
            if (status === SINGLE_KEY) return '#4e79a7';
            if (/withdraw/i.test(status)) return '#9ca3af';
            const palette = ['#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f',
                '#edc949', '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab'];
            const idx = Math.max(0, zDomain.indexOf(status));
            return palette[idx % palette.length];
        }

        function statusOrderForColors(zDomain = []) {
            const order = [];
            [currentDataset, compareDataset].forEach(dataset => {
                ((dataset && dataset.meta && dataset.meta.status) || []).forEach(status => {
                    if (!order.includes(status)) order.push(status);
                });
            });
            zDomain.forEach(status => {
                if (!order.includes(status)) order.push(status);
            });
            return order;
        }

        function buildChartData() {
            const parsed = parseEntries(args.xaxis, currentDataset);
            const currentKeys = statusKeysFor(args.view, parsed, currentDataset);
            const compareActive = !!(args.comparison.active && compareDataset && axisHasData(args.xaxis, compareDataset));
            const compareParsed = compareActive ? parseEntries(args.xaxis, compareDataset) : null;
            const compareKeys = compareActive
                ? statusKeysFor(args.view, compareParsed, compareDataset)
                : [];
            const zDomain = unionStatusKeys(currentKeys, compareKeys, [currentDataset, compareDataset]);
            const allEntries = canonicalEntryRows(parsed, currentKeys, compareParsed, compareKeys, zDomain);
            const entries = allEntries.slice(0, Math.min(Math.max(1, args.numBars), topLimit()));
            const data = rowsFor(entries, 'current', currentKeys, zDomain, parsed);
            const compareBins = compareActive
                ? rowsFor(entries, 'compare', compareKeys, zDomain, compareParsed)
                : null;
            return { parsed, compareParsed, allEntries, entries, currentKeys, compareKeys, data, compareBins, zDomain, compareActive };
        }

        function compactLabel(label) {
            const text = String(label || '');
            return text.length > 34 ? `${text.slice(0, 31)}...` : text;
        }

        function tickSpec(entries) {
            const targetTicks = args.showLabels ? 30 : 42;
            const stride = Math.max(1, Math.ceil(entries.length / targetTicks));
            const values = entries
                .map((_, i) => i + 0.5)
                .filter((_, i) => i % stride === 0);
            const format = (value) => {
                const v = Number(value);
                if (!Number.isFinite(v)) return '';
                const centerIdx = Math.round(v - 0.5);
                if (centerIdx >= 0 && centerIdx < entries.length && Math.abs(v - (centerIdx + 0.5)) < 1e-6) {
                    return args.showLabels ? compactLabel(entries[centerIdx].label) : String(centerIdx + 1);
                }
                return d3.format('d')(v);
            };
            return { values, format };
        }

        function chartMode() {
            if (args.chart === 'GroupedBar') return 'grouped';
            if (args.chart === 'OverlaidBar') return 'overlaid';
            return 'stacked';
        }

        function comparisonToken() {
            return `${args.comparison.mode}_${args.comparison.layout}`;
        }

        function currentLabel() {
            return [currentDataset.label, viewLabel(args.view)].filter(Boolean).join(' ');
        }

        function compareLabel() {
            const targetLabel = compareDataset
                ? compareDataset.label
                : [args.comparison.conf ? String(args.comparison.conf).toUpperCase() : '', args.comparison.year].filter(Boolean).join(' ');
            return [targetLabel, viewLabel(args.view)].filter(Boolean).join(' ');
        }

        function readableTextColor(fill) {
            const c = d3.color(fill);
            if (!c) return '#111827';
            const yiq = (c.r * 299 + c.g * 587 + c.b * 114) / 1000;
            return yiq < 142 ? '#fff' : '#111827';
        }

        function treemapStatusKey(status) {
            return String(status || '').toLowerCase().replace(/[_\s-]+/g, '');
        }

        function treemapIsWithdrawStatus(status) {
            return /withdraw/.test(treemapStatusKey(status));
        }

        function treemapIsDeskRejectStatus(status) {
            return /deskreject/.test(treemapStatusKey(status));
        }

        function treemapIsRejectStatus(status) {
            const key = treemapStatusKey(status);
            return /reject/.test(key) && !/deskreject/.test(key);
        }

        function treemapIsDecisionAcceptStatus(status) {
            const key = treemapStatusKey(status);
            if (!key || /active|total|before|after|unknown/.test(key)) return false;
            return !treemapIsWithdrawStatus(status)
                && !treemapIsDeskRejectStatus(status)
                && !treemapIsRejectStatus(status);
        }

        function treemapAcceptanceRate(statusCounts) {
            let accepted = 0;
            let denominator = 0;
            Object.entries(statusCounts || {}).forEach(([status, rawCount]) => {
                const count = Number(rawCount) || 0;
                if (!count || treemapIsWithdrawStatus(status) || treemapIsDeskRejectStatus(status)) return;
                if (treemapIsRejectStatus(status)) {
                    denominator += count;
                } else if (treemapIsDecisionAcceptStatus(status)) {
                    accepted += count;
                    denominator += count;
                }
            });
            return denominator > 0 ? accepted / denominator : null;
        }

        function treemapAllStatusCounts(entry, parsed, dataset = currentDataset) {
            if (parsed.summaryOnly) return {};
            const counts = {};
            (dataset.meta.status || []).forEach(status => {
                const count = countFor(entry, status, parsed);
                if (count > 0) counts[status] = count;
            });
            return counts;
        }

        function wrappedWords(text, maxChars, maxLines) {
            const words = String(text || '').split(/\s+/).filter(Boolean);
            const lines = [];
            let line = '';
            for (const wordRaw of words) {
                const word = wordRaw.length > maxChars ? `${wordRaw.slice(0, Math.max(1, maxChars - 3))}...` : wordRaw;
                const next = line ? `${line} ${word}` : word;
                if (next.length <= maxChars) {
                    line = next;
                } else {
                    if (line) lines.push(line);
                    line = word;
                }
                if (lines.length >= maxLines) break;
            }
            if (line && lines.length < maxLines) lines.push(line);
            return lines;
        }

        function formatCount(value) {
            const n = Number(value) || 0;
            if (n >= 1000000) return `${d3.format('.1f')(n / 1000000)}M`;
            if (n >= 1000) return `${d3.format('.1f')(n / 1000)}k`;
            return d3.format('d')(n);
        }

        function setComparisonGlobals(activeCompare) {
            const self = {
                conf: currentDataset.conf || '',
                year: currentDataset.year || '',
                track: currentDataset.track || 'main',
                label: currentLabel(),
            };
            window.pc_cmp_cfg = Object.assign({}, window.pc_cmp_cfg || {}, { self });
            window.pc_comparison_meta = activeCompare ? { label: compareLabel(), paperlist: true } : null;
            window.pc_comparison_merge_mode = activeCompare ? comparisonToken() : null;
        }

        function flowTargetKey() {
            return [
                currentDataset.conf || ajaxInfo.conf || '',
                currentDataset.year || ajaxInfo.year || '',
                currentDataset.track || ajaxInfo.track || 'main',
                args.view,
                Math.max(1, Math.min(TOP_CAP, Number(args.numBars) || 100)),
            ].join('|');
        }

        function ensureFlowDataset(onReady) {
            const key = flowTargetKey();
            if (flowCache.has(key)) return flowCache.get(key);
            if (flowFlights.has(key)) return null;
            const url = ((window.pc_cmp_cfg && window.pc_cmp_cfg.ajax_url) || ajaxInfo.ajax_url || '/wp-admin/admin-ajax.php')
                + '?action=pc_paperlist_flow'
                + '&conf=' + encodeURIComponent(currentDataset.conf || ajaxInfo.conf || '')
                + '&year=' + encodeURIComponent(currentDataset.year || ajaxInfo.year || '')
                + '&track=' + encodeURIComponent(currentDataset.track || ajaxInfo.track || 'main')
                + '&view=' + encodeURIComponent(args.view)
                + '&limit=' + encodeURIComponent(Math.max(1, Math.min(TOP_CAP, Number(args.numBars) || 100)));
            const flight = fetch(url, { credentials: 'same-origin' })
                .then(response => response.json())
                .then(js => {
                    if (!js || !js.success || !js.data) {
                        throw new Error((js && js.data && js.data.msg) || 'fetch failed');
                    }
                    flowCache.set(key, js.data);
                    flowError = '';
                    if (typeof onReady === 'function') onReady();
                })
                .catch(error => {
                    flowError = error.message || String(error);
                    console.error('[Paperlist flow] fetch failed:', error);
                })
                .finally(() => {
                    flowFlights.delete(key);
                });
            flowFlights.set(key, flight);
            return null;
        }

        function treemapActiveStatuses(selectedKeys, zDomain, hiddenTiers) {
            const selected = new Set(selectedKeys);
            const activeStatuses = zDomain.filter(status => selected.has(status) && !hiddenTiers.has(status));
            return activeStatuses.length ? activeStatuses : zDomain.filter(status => selected.has(status));
        }

        function treemapTotal(entries, selectedKeys, zDomain, parsed, hiddenTiers) {
            const usableStatuses = treemapActiveStatuses(selectedKeys, zDomain, hiddenTiers);
            return d3.sum(entries, entry => usableStatuses.reduce((sum, status) => sum + countFor(entry, status, parsed), 0));
        }

        function treemapRows(entries, selectedKeys, zDomain, parsed, hiddenTiers, totalOverride, dataset = currentDataset) {
            const usableStatuses = treemapActiveStatuses(selectedKeys, zDomain, hiddenTiers);
            const rows = entries.map((entry, rank) => {
                const statusCounts = {};
                let value = 0;
                usableStatuses.forEach(status => {
                    const count = countFor(entry, status, parsed);
                    if (count > 0) {
                        statusCounts[status] = count;
                        value += count;
                    }
                });
                if (value <= 0) return null;
                const allStatusCounts = treemapAllStatusCounts(entry, parsed, dataset);
                const statusSegments = zDomain
                    .filter(status => statusCounts[status] > 0 && !hiddenTiers.has(status))
                    .map(status => ({ status, count: statusCounts[status] }));
                const dominant = statusSegments.reduce((best, seg) => {
                    return !best || seg.count > best.count ? seg : best;
                }, null);
                const statusSegmentTotal = d3.sum(statusSegments, seg => seg.count) || value;
                return {
                    key: entry.key,
                    label: entry.label,
                    rank,
                    value,
                    statusCounts,
                    statusSegments,
                    statusSegmentTotal,
                    dominant: dominant ? dominant.status : usableStatuses[0],
                    acceptance_rate: parsed.summaryOnly ? null : treemapAcceptanceRate(allStatusCounts),
                };
            }).filter(Boolean);
            const total = Math.max(1, Number(totalOverride) || d3.sum(rows, d => d.value) || 1);
            rows.forEach(row => { row.percent = row.value / total; });
            return rows;
        }

        function treemapPanels(currentRows, compareRows, activeCompare, currentTotal, compareTotal, legendReserveW = 0) {
            const margin = { top: 54, right: 34, bottom: 34, left: 34 + Math.max(0, legendReserveW || 0) };
            const gap = activeCompare ? 34 : 16;
            const plot = {
                x: margin.left,
                y: margin.top,
                w: Math.max(20, args.width - margin.left - margin.right),
                h: Math.max(20, args.height - margin.top - margin.bottom),
            };
            if (!activeCompare || !compareRows.length) {
                return [{ side: 'cur', label: currentLabel(), x: plot.x, y: plot.y, w: plot.w, h: plot.h, rows: currentRows, total: currentTotal }];
            }
            const horizontal = !String(args.comparison.layout || '').endsWith('_v');
            const proportional = args.comparison.mode === 'proportional';
            const ratio = proportional && currentTotal + compareTotal > 0
                ? currentTotal / (currentTotal + compareTotal)
                : 0.5;
            if (horizontal) {
                const usableH = Math.max(20, plot.h - gap);
                const currentH = Math.max(0, usableH * ratio);
                const compareH = Math.max(0, usableH - currentH);
                return [
                    { side: 'cur', label: currentLabel(), x: plot.x, y: plot.y, w: plot.w, h: currentH, rows: currentRows, total: currentTotal },
                    { side: 'cmp', label: compareLabel(), x: plot.x, y: plot.y + currentH + gap, w: plot.w, h: compareH, rows: compareRows, total: compareTotal },
                ];
            }
            const usableW = Math.max(20, plot.w - gap);
            const currentW = Math.max(0, usableW * ratio);
            const compareW = Math.max(0, usableW - currentW);
            return [
                { side: 'cur', label: currentLabel(), x: plot.x, y: plot.y, w: currentW, h: plot.h, rows: currentRows, total: currentTotal },
                { side: 'cmp', label: compareLabel(), x: plot.x + currentW + gap, y: plot.y, w: compareW, h: plot.h, rows: compareRows, total: compareTotal },
            ];
        }

        function treemapStandaloneLegendSpec(useStandalone, legendCount, folded = false) {
            if (!useStandalone || !legendCount) return null;
            if (folded) {
                const reserveW = Math.min(156, Math.max(0, args.width - 520));
                if (reserveW < 132) return null;
                return {
                    w: reserveW - 14,
                    h: 34,
                    reserveW,
                };
            }
            const { estimatedW, estimatedH } = treemapLegendEstimate(legendCount);
            const targetW = Math.min(Math.max(210, estimatedW), Math.max(180, args.width * 0.24));
            const legendH = Math.max(180, args.height - 88, estimatedH);
            const reserveLimit = Math.max(0, args.width - 520);
            const reserveW = Math.min(targetW + 14, reserveLimit);
            if (reserveW < 180) return null;
            return {
                w: Math.max(166, reserveW - 14),
                h: legendH,
                reserveW,
            };
        }

        function treemapStandaloneLegendNode(spec) {
            if (!spec) return null;
            const x0 = 34;
            const y0 = 54;
            return {
                x0,
                y0,
                x1: x0 + spec.w,
                y1: Math.min(args.height - 34, y0 + spec.h),
                panel: { side: 'legend', label: 'Legends', total: 1, rows: [] },
                data: {
                    key: '__legend_standalone__',
                    label: 'Legends',
                    value: 1,
                    percent: 0,
                    statusCounts: {},
                    statusSegments: [],
                    dominant: '',
                    isLegend: true,
                },
            };
        }

        function treemapLegendEstimate(legendCount) {
            const count = Math.max(1, Number(legendCount) || 1);
            const estimatedCols = count >= 8 ? 2 : 1;
            const estimatedRows = Math.ceil(count / estimatedCols);
            const rowH = 18;
            return {
                estimatedW: estimatedCols > 1 ? 260 : 210,
                estimatedH: 204 + estimatedRows * rowH,
                rowH,
            };
        }

        function treemapLegendDatum(value) {
            return {
                key: '__legend__',
                label: 'Legends',
                value,
                percent: 0,
                statusCounts: {},
                statusSegments: [],
                dominant: '',
                isLegend: true,
            };
        }

        function treemapNodeSort(a, b) {
            if (a.data && a.data.isLegend) return -1;
            if (b.data && b.data.isLegend) return 1;
            return (b.value || 0) - (a.value || 0);
        }

        function treemapLegendContentHeight(legendCount, widthHint) {
            const count = Math.max(1, Number(legendCount) || 1);
            const pad = 10;
            const itemIndent = 12;
            const rowH = treemapLegendEstimate(count).rowH;
            const availW = Math.max(42, (Number(widthHint) || 210) - pad * 2 - itemIndent);
            const cols = Math.max(1, Math.min(4, Math.floor(availW / 112), count));
            const tierRowCount = Math.ceil(count / cols);
            return 204 + tierRowCount * rowH;
        }

        function treemapLegendDims(rows, legendValue, panel) {
            const root = d3.hierarchy({ children: (rows || []).concat([treemapLegendDatum(legendValue)]) })
                .sum(d => d.value)
                .sort(treemapNodeSort);
            d3.treemap()
                .tile(d3.treemapSquarify.ratio(1.12))
                .size([Math.max(1, panel.w), Math.max(1, panel.h)])
                .paddingInner(2)
                .round(true)(root);
            const node = root.leaves().find(leaf => leaf.data && leaf.data.isLegend);
            if (!node) return { w: 0, h: 0 };
            return {
                w: Math.max(0, node.x1 - node.x0),
                h: Math.max(0, node.y1 - node.y0),
            };
        }

        function treemapLegendValue(rows, activeCompare, legendCount, panel, folded = false) {
            const total = d3.sum(rows || [], d => d.value || 0);
            if (!total) return 1;
            const { estimatedW } = treemapLegendEstimate(legendCount);
            const panelW = Math.max(1, Number(panel && panel.w) || estimatedW);
            const panelH = Math.max(1, Number(panel && panel.h) || 260);
            const minW = folded
                ? Math.min(96, Math.max(82, panelW * 0.10))
                : Math.min(Math.max(148, estimatedW * 0.72), Math.max(90, panelW * 0.46));
            const maxRatio = folded ? (activeCompare ? 0.06 : 0.04) : (activeCompare ? 0.40 : 0.34);
            let best = null;
            for (let i = 0; i < 28; i++) {
                const t = i / 27;
                const minRatio = folded ? 0.001 : 0.01;
                const ratio = minRatio + (maxRatio - minRatio) * Math.pow(t, folded ? 1.05 : 1.18);
                const value = total * ratio / Math.max(0.01, 1 - ratio);
                const dims = treemapLegendDims(rows, value, panel);
                const targetH = folded
                    ? Math.min(30, Math.max(24, panelH * 0.06))
                    : Math.min(
                        Math.max(186, treemapLegendContentHeight(legendCount, dims.w) + 6),
                        Math.max(110, panelH * 0.82)
                    );
                const underW = Math.max(0, minW - dims.w);
                const underH = Math.max(0, targetH - dims.h);
                const extraH = Math.max(0, dims.h - targetH);
                const extraW = Math.max(0, dims.w - Math.max(minW, folded ? 90 : estimatedW * 0.95));
                const score = underH * 1000 + underW * 700 + extraH * (folded ? 10 : 1.55) + extraW * 0.22 + ratio * (folded ? 220 : 30);
                if (!best || score < best.score) best = { value, score };
            }
            return best ? best.value : Math.max(1, total * 0.08);
        }

        function drawPaperlistTileChart(g, node, fillForStatus, innerScale = {}) {
            const inner = g.select('g.pc-paperlist-treemap-inner');
            inner.selectAll('*').remove();
            const mode = TILE_CHART_TYPES.includes(args.tileChart) ? args.tileChart : 'Status pie';
            if (mode === 'None') return 0;
            const d = node.data;
            const w = Math.max(0, node.x1 - node.x0);
            const h = Math.max(0, node.y1 - node.y0);
            const segments = (d.statusSegments || []).filter(seg => (Number(seg.count) || 0) > 0);
            if (!segments.length || w < 30 || h < 24) return 0;

            if (mode === 'Status pie') {
                if (w < 34 || h < 30) return 0;
                const margin = Math.max(2, Math.min(6, Math.sqrt(w * h) * 0.018));
                const maxValue = Math.max(1, Number(innerScale.pieMaxValue) || Number(d.value) || 1);
                const valueRatio = Math.max(0.08, Math.min(1, (Number(d.value) || 0) / maxValue));
                const maxSize = Math.min(68, w - margin * 2, h - margin * 2);
                const minSize = Math.min(maxSize, Math.max(10, Math.min(18, maxSize * 0.38)));
                const scaledSize = maxSize * 0.88 * Math.sqrt(valueRatio);
                const size = Math.max(minSize, Math.min(maxSize, scaledSize));
                if (size < 10) return 0;
                const cx = Math.max(margin + size / 2, w - margin - size / 2);
                const cy = Math.max(margin + size / 2, h - margin - size / 2);
                const pie = d3.pie()
                    .value(seg => Number(seg.count) || 0)
                    .sort(null)(segments);
                const arc = d3.arc()
                    .innerRadius(size * 0.26)
                    .outerRadius(size / 2);
                const pieG = inner.append('g')
                    .attr('class', 'pc-paperlist-treemap-inner-pie')
                    .attr('transform', `translate(${cx},${cy})`);
                pieG.selectAll('path')
                    .data(pie, seg => seg.data.status)
                    .join('path')
                    .attr('class', 'pc-paperlist-treemap-inner-mark pc-paperlist-treemap-inner-slice')
                    .attr('data-status', seg => seg.data.status)
                    .attr('d', arc)
                    .attr('fill', seg => fillForStatus(seg.data.status))
                    .attr('stroke', 'rgba(255,255,255,0.88)')
                    .attr('stroke-width', Math.max(0.45, Math.min(0.8, size / 42)))
                    .attr('opacity', 0.92);
                return 0;
            }

            if (mode === 'Status grouped') {
                if (w < 58 || h < 46) return 0;
                const groupedStatuses = (innerScale.groupedStatuses || segments.map(seg => seg.status)).filter(Boolean);
                const groupedSegments = groupedStatuses.map(status => ({
                    status,
                    count: Number(d.statusCounts && d.statusCounts[status]) || 0,
                }));
                if (!groupedSegments.length) return 0;
                const chartH = Math.max(18, Math.min(54, h * 0.34));
                const pad = 5;
                const yBase = h - pad;
                const showAxisLabels = w >= 132 && chartH >= 26;
                const axisLabelW = showAxisLabels ? 22 : 0;
                const axisX = Math.max(pad + 10, w - pad - axisLabelW);
                const chartW = Math.max(1, axisX - pad - 4);
                const groupStep = chartW / groupedSegments.length;
                const barW = Math.max(2, groupStep - 2);
                const scaleMax = Math.max(1, Number(innerScale.groupedMax) || 1);
                const localMax = d3.max(groupedSegments, seg => Number(seg.count) || 0) || 0;
                const axisTop = yBase - chartH;
                inner.append('line')
                    .attr('class', 'pc-paperlist-treemap-inner-axis')
                    .attr('x1', pad)
                    .attr('x2', axisX)
                    .attr('y1', yBase)
                    .attr('y2', yBase)
                    .attr('stroke', 'rgba(17,24,39,0.28)')
                    .attr('stroke-width', 1);
                inner.append('line')
                    .attr('class', 'pc-paperlist-treemap-inner-axis')
                    .attr('x1', axisX)
                    .attr('x2', axisX)
                    .attr('y1', axisTop)
                    .attr('y2', yBase)
                    .attr('stroke', 'rgba(17,24,39,0.36)')
                    .attr('stroke-width', 1);
                [axisTop, yBase].forEach(y => {
                    inner.append('line')
                        .attr('class', 'pc-paperlist-treemap-inner-axis-tick')
                        .attr('x1', axisX)
                        .attr('x2', Math.min(w - pad, axisX + 3))
                        .attr('y1', y)
                        .attr('y2', y)
                        .attr('stroke', 'rgba(17,24,39,0.36)')
                        .attr('stroke-width', 1);
                });
                if (showAxisLabels) {
                    [
                        { y: axisTop + 4, text: d3.format('.2s')(scaleMax) },
                        { y: yBase, text: '0' },
                    ].forEach(tick => {
                        inner.append('text')
                            .attr('class', 'pc-paperlist-treemap-inner-axis-label')
                            .attr('x', axisX + 4)
                            .attr('y', tick.y)
                            .attr('font-family', 'sans-serif')
                            .attr('font-size', 9)
                            .attr('fill', 'rgba(17,24,39,0.72)')
                            .text(tick.text);
                    });
                } else if (w >= 96 && localMax > 0) {
                    inner.append('text')
                        .attr('class', 'pc-paperlist-treemap-inner-axis-label')
                        .attr('x', Math.max(pad, axisX - 2))
                        .attr('y', axisTop + 4)
                        .attr('text-anchor', 'end')
                        .attr('font-family', 'sans-serif')
                        .attr('font-size', 8)
                        .attr('fill', 'rgba(17,24,39,0.62)')
                        .text(d3.format('.2s')(scaleMax));
                }
                inner.selectAll('rect.pc-paperlist-treemap-inner-bar')
                    .data(groupedSegments, seg => seg.status)
                    .join('rect')
                    .attr('class', 'pc-paperlist-treemap-inner-mark pc-paperlist-treemap-inner-bar')
                    .attr('data-status', seg => seg.status)
                    .attr('x', (_, i) => pad + i * groupStep + 1)
                    .attr('y', seg => {
                        const count = Number(seg.count) || 0;
                        return yBase - (count > 0 ? Math.max(1, chartH * (count / scaleMax)) : 0);
                    })
                    .attr('width', barW)
                    .attr('height', seg => {
                        const count = Number(seg.count) || 0;
                        return count > 0 ? Math.max(1, chartH * (count / scaleMax)) : 0;
                    })
                    .attr('fill', seg => fillForStatus(seg.status))
                    .attr('opacity', 0.88);
                return chartH + pad * 2;
            }

            const stripH = Math.max(6, Math.min(22, h * 0.2));
            let x = 0;
            const segmentTotal = Math.max(1, Number(d.statusSegmentTotal) || d3.sum(segments, seg => Number(seg.count) || 0) || d.value);
            inner.selectAll('rect.pc-paperlist-treemap-inner-strip')
                .data(segments, seg => seg.status)
                .join('rect')
                .attr('class', 'pc-paperlist-treemap-inner-mark pc-paperlist-treemap-inner-strip')
                .attr('data-status', seg => seg.status)
                .attr('x', seg => {
                    const x0 = x;
                    x += w * (seg.count / segmentTotal);
                    return x0;
                })
                .attr('y', Math.max(0, h - stripH))
                .attr('width', seg => Math.max(0, w * (seg.count / segmentTotal)))
                .attr('height', stripH)
                .attr('fill', seg => fillForStatus(seg.status))
                .attr('opacity', 0.94);
            return stripH + 2;
        }

        function drawPaperlistTreemapLegendCell(g, node, zDomain, hiddenTiers, fillForStatus, chartPayload, acceptanceFillScale, body, rootNode) {
            const legendData = zDomain.slice().reverse();
            g.select('g.pc-paperlist-treemap-inner').selectAll('*').remove();
            g.select('g.pc-paperlist-treemap-status-strip').selectAll('*').remove();
            const labelG = g.select('g.pc-paperlist-treemap-labels');
            labelG.selectAll('*').remove();
            labelG.attr('pointer-events', 'all');

            const pad = 10;
            const w = Math.max(1, node.x1 - node.x0);
            const fitText = (text, maxWidth, charWidth) => {
                const raw = String(text || '');
                const maxChars = Math.max(4, Math.floor(Math.max(0, maxWidth) / charWidth));
                return raw.length > maxChars ? `${raw.slice(0, Math.max(1, maxChars - 3))}...` : raw;
            };
            const sectionText = (x, y, text) => {
                labelG.append('text')
                    .attr('x', x)
                    .attr('y', y)
                    .attr('font-family', 'sans-serif')
                    .attr('font-size', 13)
                    .attr('font-style', 'italic')
                    .attr('fill', '#888')
                    .text(text);
            };
            const checkbox = (cls, y, label, checked, onClick) => {
                const row = labelG.append('g')
                    .attr('class', cls)
                    .attr('transform', `translate(${pad + 12},${y})`)
                    .style('cursor', 'pointer')
                    .on('click', function (event) {
                        if (event && event.stopPropagation) event.stopPropagation();
                        onClick();
                    });
                row.append('rect')
                    .attr('width', 14)
                    .attr('height', 14)
                    .attr('rx', 2)
                    .attr('ry', 2)
                    .attr('fill', '#fff')
                    .attr('stroke', '#777')
                    .attr('stroke-width', 1.2);
                row.append('path')
                    .attr('class', cls.indexOf('help') >= 0 ? 'pc-help-note-check' : 'pc-toggle-check')
                    .attr('d', 'M 3 7 L 6 10 L 11 4')
                    .attr('fill', 'none')
                    .attr('stroke', '#333')
                    .attr('stroke-width', 2)
                    .attr('stroke-linejoin', 'round')
                    .attr('stroke-linecap', 'round')
                    .attr('opacity', checked ? 1 : 0);
                row.append('text')
                    .attr('x', 20)
                    .attr('y', 11)
                    .attr('font-size', 12)
                    .attr('font-family', 'sans-serif')
                    .attr('fill', '#555')
                    .text(fitText(label, w - pad * 2 - 34, 5.8));
            };
            const settingsRow = (y) => {
                const GEAR_PATH_TREEMAP = "M12 15.5A3.5 3.5 0 018.5 12 3.5 3.5 0 0112 8.5a3.5 3.5 0 013.5 3.5 3.5 3.5 0 01-3.5 3.5m7.43-2.53c.04-.32.07-.64.07-.97 0-.33-.03-.66-.07-1l2.11-1.63c.19-.15.24-.42.12-.64l-2-3.46a.5.5 0 00-.61-.22l-2.49 1c-.52-.39-1.06-.73-1.69-.98l-.37-2.65A.506.506 0 0014 2h-4c-.25 0-.46.18-.5.42l-.37 2.65c-.63.25-1.17.59-1.69.98l-2.49-1a.5.5 0 00-.61.22l-2 3.46c-.13.22-.07.49.12.64L4.57 11c-.04.34-.07.67-.07 1 0 .33.03.65.07.97l-2.11 1.66c-.19.15-.25.42-.12.64l2 3.46c.12.22.39.31.61.22l2.49-1.01c.52.4 1.06.74 1.69.99l.37 2.65c.04.24.25.42.5.42h4c.25 0 .46-.18.5-.42l.37-2.65c.63-.26 1.17-.59 1.69-.99l2.49 1.01a.5.5 0 00.61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.66z";
                const row = labelG.append('g')
                    .attr('class', 'pc-paperlist-treemap-settings')
                    .attr('transform', `translate(${pad + 12},${y})`)
                    .style('cursor', 'pointer')
                    .style('pointer-events', 'all')
                    .on('mouseenter', function () {
                        d3.select(this).select('path.pc-settings-gear-path').style('transform', 'rotate(120deg)');
                        const btn = document.getElementById('pc_btn_settings');
                        if (btn) btn.classList.add('pc-gear-hover');
                    })
                    .on('mouseleave', function () {
                        d3.select(this).select('path.pc-settings-gear-path').style('transform', 'rotate(0deg)');
                        const btn = document.getElementById('pc_btn_settings');
                        if (btn) btn.classList.remove('pc-gear-hover');
                    })
                    .on('click', function (event) {
                        if (event && event.stopPropagation) event.stopPropagation();
                        onclickPaperlistSetting();
                    });
                row.append('g')
                    .attr('class', 'pc-settings-gear')
                    .attr('transform', `scale(${13/16}) translate(-3.5,-3.5)`)
                    .append('path')
                    .attr('class', 'pc-settings-gear-path')
                    .attr('d', GEAR_PATH_TREEMAP)
                    .attr('fill', '#333')
                    .attr('stroke', 'none')
                    .style('transform-origin', '12px 12px')
                    .style('transition', 'transform 600ms ease');
                row.append('text')
                    .attr('x', 20)
                    .attr('y', 11)
                    .attr('font-size', 12)
                    .attr('font-family', 'sans-serif')
                    .attr('fill', '#555')
                    .text(fitText('Settings [S]', w - pad * 2 - 32, 5.8));
            };
            const drawNotesPopup = (helpRowY) => {
                const notes = [
                    'Notes:',
                    '1. Tile area scales with paper count.',
                    '2. Tile color maps to acceptance rate.',
                    '3. Grouped inner bars share one scale across tiles.',
                    'Press [S] or click gear to toggle settings.',
                ];
                const notesPadX = 12;
                const notesPadY = 10;
                const notesLineH = 15;
                const notesW = Math.min(500, Math.max(300, args.width - 80));
                const notesH = notes.length * notesLineH + notesPadY * 2 + 4;
                let gNotesPopup = body.select('g.pc-paperlist-notes-popup');
                if (gNotesPopup.empty()) {
                    gNotesPopup = body.append('g').attr('class', 'pc-paperlist-notes-popup');
                    gNotesPopup.append('rect').attr('class', 'pc-notes-bg')
                        .attr('rx', 4)
                        .attr('ry', 4)
                        .attr('fill', 'rgba(255,255,255,0.94)')
                        .attr('stroke', 'rgba(0,0,0,0.18)')
                        .attr('stroke-width', 1);
                    const closeBtn = gNotesPopup.append('g')
                        .attr('class', 'pc-notes-close')
                        .style('cursor', 'pointer')
                        .on('click', function (event) {
                            if (event && event.stopPropagation) event.stopPropagation();
                            rootNode.__pc_help_note_visible = false;
                            labelG.select('g.pc-paperlist-treemap-help path.pc-help-note-check').attr('opacity', 0);
                            gNotesPopup.style('display', 'none');
                        });
                    closeBtn.append('circle')
                        .attr('r', 9)
                        .attr('fill', '#fff')
                        .attr('stroke', '#888')
                        .attr('stroke-width', 1);
                    closeBtn.append('path')
                        .attr('d', 'M -3.5 -3.5 L 3.5 3.5 M -3.5 3.5 L 3.5 -3.5')
                        .attr('stroke', '#555')
                        .attr('stroke-width', 1.5)
                        .attr('stroke-linecap', 'round');
                    gNotesPopup.append('g').attr('class', 'pc-notes-lines');
                }
                const rightX = node.x1 + 8;
                const leftX = node.x0 - notesW - 8;
                const popupX = rightX + notesW <= args.width - 8
                    ? rightX
                    : Math.max(8, Math.min(leftX, args.width - notesW - 8));
                const preferredY = node.y0 + helpRowY - 6;
                const popupY = Math.max(8, Math.min(preferredY, args.height - notesH - 8));
                gNotesPopup.attr('transform', `translate(${popupX},${popupY})`)
                    .style('display', rootNode.__pc_help_note_visible ? null : 'none')
                    .raise();
                gNotesPopup.select('rect.pc-notes-bg').attr('width', notesW).attr('height', notesH);
                gNotesPopup.select('g.pc-notes-close').attr('transform', `translate(${notesW - 14},14)`);
                const noteLines = gNotesPopup.select('g.pc-notes-lines')
                    .selectAll('text.pc-note-line')
                    .data(notes);
                noteLines.exit().remove();
                noteLines.enter()
                    .append('text')
                    .attr('class', 'pc-note-line')
                    .attr('text-anchor', 'start')
                    .attr('fill', '#333')
                    .attr('font-size', 12)
                    .attr('font-family', 'sans-serif')
                    .attr('x', notesPadX)
                  .merge(noteLines)
                    .attr('y', (_, i) => notesPadY + notesLineH * (i + 1) - 4)
                    .attr('font-weight', (_, i) => i === notes.length - 1 ? 'bold' : 'normal')
                    .text(d => d);
            };

            const folded = !!rootNode.__pc_paperlist_treemap_legend_folded;
            const titleY = pad + 13;
            const titleG = labelG.append('g')
                .attr('class', 'pc-paperlist-treemap-legend-title')
                .style('cursor', 'pointer')
                .style('pointer-events', 'all')
                .on('click', function (event) {
                    if (event && event.stopPropagation) event.stopPropagation();
                    rootNode.__pc_paperlist_treemap_legend_folded = !folded;
                    renderPaperlistTreemap(chartPayload);
                });
            const titleText = titleG.append('text')
                .attr('x', pad)
                .attr('y', titleY)
                .attr('font-family', 'sans-serif')
                .attr('font-size', 13)
                .attr('font-weight', 800)
                .attr('fill', '#334155');
            titleText.append('tspan')
                .attr('class', 'pc-paperlist-treemap-legend-title-main')
                .text(fitText('Legends', w - pad * 2 - 22, 7.2));
            titleText.append('tspan')
                .attr('class', 'pc-paperlist-treemap-legend-title-chevron')
                .attr('dx', 5)
                .text(folded ? '▸' : '▾');
            titleG.append('title').text(folded ? 'Expand legend' : 'Fold legend');
            if (folded) return;

            const rowW = Math.max(60, w - pad * 2);
            const visualY = titleY + 22;
            sectionText(pad, visualY, 'Visuals');
            labelG.append('text')
                .attr('x', pad)
                .attr('y', visualY + 13)
                .attr('font-size', 10)
                .attr('font-family', 'sans-serif')
                .attr('fill', '#aaa')
                .text(fitText('click to toggle display options', w - pad * 2, 4.9));
            const helpRowY = visualY + 31;
            checkbox('pc-paperlist-treemap-help', helpRowY, 'Help Note', !!rootNode.__pc_help_note_visible, () => {
                rootNode.__pc_help_note_visible = !rootNode.__pc_help_note_visible;
                labelG.select('g.pc-paperlist-treemap-help path.pc-help-note-check')
                    .attr('opacity', rootNode.__pc_help_note_visible ? 1 : 0);
                drawNotesPopup(helpRowY);
            });
            settingsRow(helpRowY + 20);

            const tiersY = visualY + 82;
            sectionText(pad, tiersY, 'Tiers');
            labelG.append('text')
                .attr('x', pad)
                .attr('y', tiersY + 13)
                .attr('font-size', 10)
                .attr('font-family', 'sans-serif')
                .attr('fill', '#aaa')
                .text(fitText('click hide · Ctrl+click solo', w - pad * 2, 4.9));
            const startY = tiersY + 24;
            const itemIndent = 12;
            const { rowH } = treemapLegendEstimate(legendData.length);
            const availW = Math.max(42, w - pad * 2 - itemIndent);
            const cols = Math.max(1, Math.min(4, Math.floor(availW / 112), legendData.length || 1));
            const colW = availW / cols;
            const rows = labelG.selectAll('g.pc-paperlist-treemap-legend-row')
                .data(legendData, d => d)
                .join('g')
                .attr('class', 'pc-paperlist-treemap-legend-row')
                .attr('transform', (_, i) => {
                    const col = i % cols;
                    const row = Math.floor(i / cols);
                    return `translate(${pad + itemIndent + col * colW},${startY + row * rowH})`;
                })
                .style('cursor', 'pointer')
                .on('click', function (event, status) {
                    if (event && event.stopPropagation) event.stopPropagation();
                    if (event.ctrlKey || event.metaKey) {
                        const soloed = legendData.every(s => s === status || hiddenTiers.has(s)) && !hiddenTiers.has(status);
                        hiddenTiers.clear();
                        if (!soloed) legendData.forEach(s => { if (s !== status) hiddenTiers.add(s); });
                    } else if (hiddenTiers.has(status)) {
                        hiddenTiers.delete(status);
                    } else if (legendData.filter(s => !hiddenTiers.has(s)).length > 1) {
                        hiddenTiers.add(status);
                    }
                    renderPaperlistTreemap(chartPayload);
                });
            rows.append('rect')
                .attr('width', 14)
                .attr('height', 14)
                .attr('rx', 0)
                .attr('ry', 0)
                .attr('fill', d => fillForStatus(d))
                .attr('stroke', d => hiddenTiers.has(d) ? '#888' : 'none')
                .attr('stroke-width', 1)
                .attr('fill-opacity', d => hiddenTiers.has(d) ? 0 : 1);
            rows.append('text')
                .attr('x', 20)
                .attr('y', 11)
                .attr('font-family', 'sans-serif')
                .attr('font-size', 12)
                .attr('fill', '#333')
                .attr('text-decoration', d => hiddenTiers.has(d) ? 'line-through' : null)
                .text(d => fitText(d, colW - 24, 6.2));
            const tierRowCount = Math.ceil(legendData.length / cols);
            const accY = startY + tierRowCount * rowH + 24;
            sectionText(pad, accY, 'Acc. Rate');
            const gradX = pad + 12;
            const gradY = accY + 12;
            const gradW = Math.min(154, Math.max(104, rowW - 44));
            const gradH = 8;
            const gradSteps = 32;
            labelG.selectAll('rect.pc-paperlist-ac-rate-swatch')
                .data(d3.range(gradSteps))
                .join('rect')
                .attr('class', 'pc-paperlist-ac-rate-swatch')
                .attr('x', (_, i) => gradX + i * gradW / gradSteps)
                .attr('y', gradY)
                .attr('width', gradW / gradSteps + 0.6)
                .attr('height', gradH)
                .attr('fill', (_, i) => acceptanceFillScale((i / (gradSteps - 1)) * 0.5));
            labelG.append('rect')
                .attr('x', gradX)
                .attr('y', gradY)
                .attr('width', gradW)
                .attr('height', gradH)
                .attr('fill', 'none')
                .attr('stroke', 'rgba(15,23,42,0.2)')
                .attr('stroke-width', 0.8);
            [
                { x: gradX, text: '0%', anchor: 'start' },
                { x: gradX + gradW / 2, text: '25%', anchor: 'middle' },
                { x: gradX + gradW, text: '50%+', anchor: 'end' },
            ].forEach(tick => {
                labelG.append('text')
                    .attr('x', tick.x)
                    .attr('y', gradY + 20)
                    .attr('text-anchor', tick.anchor)
                    .attr('font-size', 9)
                    .attr('font-family', 'sans-serif')
                    .attr('fill', '#64748b')
                    .text(tick.text);
            });
            drawNotesPopup(helpRowY);
        }

        function renderPaperlistFlowChart(flowPayload) {
            const rows = (flowPayload && Array.isArray(flowPayload.rows) ? flowPayload.rows : [])
                .map(row => ({
                    country: String(row.country || 'Unknown'),
                    affiliation: String(row.affiliation || 'Unknown'),
                    author: String(row.author || 'Unknown'),
                    status: String(row.status || 'Unknown'),
                    count: Number(row.count) || 0,
                }))
                .filter(row => row.count > 0);
            if (!rows.length) {
                showEmpty(flowError || 'No relationship data available for this paperlist view.');
                return;
            }

            setComparisonGlobals(false);
            const host = d3.select('#main-render');
            host.selectAll('div.pc-empty').remove();
            let svg = host.selectAll('svg.pc-chart-shared').data([1]);
            svg = svg.join('svg')
                .attr('class', 'pc-chart-shared')
                .attr('role', 'img');
            svg.interrupt();
            svg.attr('width', args.width)
                .attr('height', args.height)
                .attr('viewBox', [0, 0, args.width, args.height])
                .style('max-width', '100%')
                .style('height', 'auto');
            svg.selectAll('*').interrupt().remove();

            const body = svg.append('g').attr('class', 'pc-body-paperlist-flow');
            const margin = {
                top: 90,
                right: Math.max(150, Math.min(230, args.width * 0.18)),
                bottom: 38,
                left: Math.max(126, Math.min(190, args.width * 0.15)),
            };
            const layers = [
                { key: 'country', label: 'Country' },
                { key: 'affiliation', label: 'Affiliation' },
                { key: 'author', label: 'Author' },
                { key: 'status', label: 'Tier' },
            ];
            const plot = {
                x0: margin.left,
                y0: margin.top,
                x1: Math.max(margin.left + 40, args.width - margin.right),
                y1: Math.max(margin.top + 60, args.height - margin.bottom),
            };
            const nodeW = 14;
            const nodeMap = new Map();
            const linkMap = new Map();
            const statusDomain = Array.from(new Set(rows.map(row => row.status)));
            const colorOrder = statusOrderForColors(statusDomain);
            const tierColorMap = typeof window.pcTierColorMap === 'function'
                ? window.pcTierColorMap(colorOrder, statusDomain)
                : Object.fromEntries(statusDomain.map(status => [status, colorFor(status, statusDomain)]));
            const nodeColor = node => {
                if (/not provided|not mapped|unknown/i.test(node.label)) return '#94a3b8';
                if (node.layer === 3) return tierColorMap[node.label] || colorFor(node.label, statusDomain);
                if (node.layer === 0) return '#52616f';
                if (node.layer === 1) return '#2f7d95';
                return '#7a5c9e';
            };
            const addNode = (layer, label) => {
                const id = `${layer}|${label}`;
                if (!nodeMap.has(id)) {
                    nodeMap.set(id, { id, layer, label, valueIn: 0, valueOut: 0, value: 0, sourceLinks: [], targetLinks: [] });
                }
                return nodeMap.get(id);
            };
            const addLink = (source, target, status, value) => {
                const id = `${source.id}>${target.id}|${status}`;
                let link = linkMap.get(id);
                if (!link) {
                    link = { id, source, target, status, value: 0 };
                    linkMap.set(id, link);
                    source.sourceLinks.push(link);
                    target.targetLinks.push(link);
                }
                link.value += value;
                source.valueOut += value;
                target.valueIn += value;
            };
            rows.forEach(row => {
                const country = addNode(0, row.country);
                const affiliation = addNode(1, row.affiliation);
                const author = addNode(2, row.author);
                const tier = addNode(3, row.status);
                addLink(country, affiliation, row.status, row.count);
                addLink(affiliation, author, row.status, row.count);
                addLink(author, tier, row.status, row.count);
            });
            const nodes = Array.from(nodeMap.values());
            const links = Array.from(linkMap.values()).filter(link => link.value > 0);
            nodes.forEach(node => {
                node.value = Math.max(node.valueIn, node.valueOut);
            });
            const isUnmappedLabel = label => /not provided|not mapped|unknown/i.test(String(label || ''));
            const layerNodes = layers.map((_, layer) => nodes
                .filter(node => node.layer === layer)
                .sort((a, b) => d3.ascending(isUnmappedLabel(a.label), isUnmappedLabel(b.label))
                    || d3.descending(a.value, b.value)
                    || d3.ascending(a.label, b.label)));
            const plotH = Math.max(40, plot.y1 - plot.y0);
            const maxLayerCount = d3.max(layerNodes, layer => layer.length) || 1;
            const gap = Math.max(2, Math.min(9, plotH / Math.max(12, maxLayerCount * 4)));
            const k = d3.min(layerNodes, layer => {
                const total = d3.sum(layer, node => node.value);
                if (!total) return Infinity;
                return Math.max(1, plotH - gap * Math.max(0, layer.length - 1)) / total;
            }) || 1;
            const x = d3.scalePoint()
                .domain(layers.map(layer => layer.label))
                .range([plot.x0, plot.x1])
                .padding(0);
            layerNodes.forEach((layer, layerIdx) => {
                const used = d3.sum(layer, node => Math.max(1, node.value * k)) + gap * Math.max(0, layer.length - 1);
                let y = plot.y0 + Math.max(0, (plotH - used) / 2);
                layer.forEach((node, rank) => {
                    const h = Math.max(1, node.value * k);
                    node.x0 = x(layers[layerIdx].label);
                    node.x1 = node.x0 + nodeW;
                    node.y0 = y;
                    node.y1 = y + h;
                    node.rank = rank;
                    y += h + gap;
                });
            });
            const linkOrder = (a, b) => d3.ascending(a.status, b.status) || d3.ascending(a.target.y0, b.target.y0);
            nodes.forEach(node => {
                let outY = node.y0;
                node.sourceLinks.sort(linkOrder).forEach(link => {
                    const h = Math.max(0, link.value * k);
                    link.y0 = outY + h / 2;
                    link.width = Math.max(0.8, h);
                    outY += h;
                });
                let inY = node.y0;
                node.targetLinks.sort((a, b) => d3.ascending(a.source.y0, b.source.y0) || d3.ascending(a.status, b.status)).forEach(link => {
                    const h = Math.max(0, link.value * k);
                    link.y1 = inY + h / 2;
                    link.width = Math.max(0.8, h);
                    inY += h;
                });
            });

            const flowValueText = value => {
                const n = Number(value) || 0;
                return Math.abs(n - Math.round(n)) < 1e-6 ? formatCount(Math.round(n)) : d3.format('.1f')(n);
            };
            const ribbon = link => {
                const x0 = link.source.x1;
                const x1 = link.target.x0;
                const xi = d3.interpolateNumber(x0, x1);
                const x2 = xi(0.46);
                const x3 = xi(0.54);
                const half = Math.max(0.45, link.width / 2);
                return [
                    `M${x0},${link.y0 - half}`,
                    `C${x2},${link.y0 - half} ${x3},${link.y1 - half} ${x1},${link.y1 - half}`,
                    `L${x1},${link.y1 + half}`,
                    `C${x3},${link.y1 + half} ${x2},${link.y0 + half} ${x0},${link.y0 + half}`,
                    'Z',
                ].join(' ');
            };
            const linkColor = link => {
                const c = d3.color(tierColorMap[link.status] || colorFor(link.status, statusDomain));
                if (!c) return '#6366f1';
                c.opacity = 1;
                return c.formatRgb();
            };

            body.append('text')
                .attr('x', margin.left)
                .attr('y', 27)
                .attr('font-size', 16)
                .attr('font-weight', 800)
                .attr('fill', '#1f2937')
                .text('Relationship Flow');
            body.append('text')
                .attr('x', margin.left)
                .attr('y', 46)
                .attr('font-size', 11)
                .attr('fill', '#64748b')
                .text(`${currentLabel()} · Top ${flowPayload.shown_authors || args.numBars} authors · ${flowValueText(flowPayload.shown_weight || d3.sum(rows, row => row.count))} authorships`);
            const coverageNotes = [];
            if ((Number(flowPayload.shown_unmapped_country_weight) || 0) > 0) coverageNotes.push(`${flowValueText(flowPayload.shown_unmapped_country_weight)} country not mapped`);
            if ((Number(flowPayload.shown_unmapped_affiliation_weight) || 0) > 0) coverageNotes.push(`${flowValueText(flowPayload.shown_unmapped_affiliation_weight)} affiliation not provided`);
            if (coverageNotes.length) {
                body.append('text')
                    .attr('x', margin.left)
                    .attr('y', 62)
                    .attr('font-size', 10)
                    .attr('fill', '#8b5e34')
                    .text(coverageNotes.join(' · '));
            }
            layers.forEach(layer => {
                body.append('text')
                    .attr('class', 'pc-paperlist-flow-layer-label')
                    .attr('x', x(layer.label) + nodeW / 2)
                    .attr('y', margin.top - 16)
                    .attr('text-anchor', 'middle')
                    .attr('font-size', 12)
                    .attr('font-weight', 800)
                    .attr('fill', '#475569')
                    .text(layer.label);
            });

            const linkG = body.append('g').attr('class', 'pc-paperlist-flow-links');
            const linkPaths = linkG.selectAll('path.pc-paperlist-flow-link')
                .data(links, link => link.id)
                .join('path')
                .attr('class', 'pc-paperlist-flow-link')
                .attr('d', ribbon)
                .attr('fill', linkColor)
                .attr('fill-opacity', 0.34)
                .attr('stroke', linkColor)
                .attr('stroke-opacity', 0.16)
                .attr('stroke-width', 0.35)
                .style('cursor', 'default');
            linkPaths.append('title')
                .text(link => `${link.source.label} -> ${link.target.label}\n${link.status}: ${flowValueText(link.value)}`);

            const nodeG = body.append('g').attr('class', 'pc-paperlist-flow-nodes')
                .selectAll('g.pc-paperlist-flow-node')
                .data(nodes, node => node.id)
                .join('g')
                .attr('class', 'pc-paperlist-flow-node')
                .attr('transform', node => `translate(${node.x0},${node.y0})`)
                .style('cursor', 'default');
            nodeG.append('rect')
                .attr('width', nodeW)
                .attr('height', node => Math.max(1, node.y1 - node.y0))
                .attr('rx', 2)
                .attr('ry', 2)
                .attr('fill', nodeColor)
                .attr('stroke', 'rgba(15,23,42,0.18)');
            nodeG.append('title')
                .text(node => `${layers[node.layer].label}: ${node.label}\n${flowValueText(node.value)} authorships`);
            const visibleLabelIds = new Set();
            const labelCaps = [12, 14, 16, 8];
            layerNodes.forEach((layer, layerIdx) => {
                let lastY = -Infinity;
                const minGap = layerIdx === 3 ? 17 : 18;
                layer.forEach(node => {
                    const h = node.y1 - node.y0;
                    const center = (node.y0 + node.y1) / 2;
                    if (!(node.layer === 3 || h >= 11 || node.rank < labelCaps[layerIdx])) return;
                    if (center - lastY < minGap) return;
                    visibleLabelIds.add(node.id);
                    lastY = center;
                });
            });
            const flowCompactLabel = node => {
                const limits = [20, 30, 24, 26];
                const text = String(node.label || '');
                const max = limits[node.layer] || 24;
                return text.length > max ? `${text.slice(0, Math.max(1, max - 3))}...` : text;
            };
            nodeG.filter(node => visibleLabelIds.has(node.id)).append('text')
                .attr('class', 'pc-paperlist-flow-label')
                .attr('x', node => node.layer === 0 ? -7 : nodeW + 7)
                .attr('y', node => (node.y1 - node.y0) / 2 + 4)
                .attr('text-anchor', node => node.layer === 0 ? 'end' : 'start')
                .attr('font-size', node => node.layer === 3 ? 12 : 10.5)
                .attr('font-weight', node => node.layer === 3 ? 750 : 650)
                .attr('fill', '#334155')
                .attr('paint-order', 'stroke')
                .attr('stroke', 'rgba(255,255,255,0.9)')
                .attr('stroke-width', 3)
                .attr('stroke-linejoin', 'round')
                .text(flowCompactLabel);

            const connectedLinkIds = node => new Set(node.sourceLinks.concat(node.targetLinks).map(link => link.id));
            const applyHover = (node = null, link = null) => {
                const activeIds = node ? connectedLinkIds(node) : (link ? new Set([link.id]) : null);
                linkPaths
                    .attr('fill-opacity', d => !activeIds ? 0.34 : (activeIds.has(d.id) ? 0.72 : 0.08))
                    .attr('stroke-opacity', d => !activeIds ? 0.16 : (activeIds.has(d.id) ? 0.38 : 0))
                    .attr('stroke-width', d => activeIds && activeIds.has(d.id) ? 0.9 : 0.35);
                nodeG.attr('opacity', d => {
                    if (!activeIds) return 1;
                    if (node && d.id === node.id) return 1;
                    return d.sourceLinks.concat(d.targetLinks).some(item => activeIds.has(item.id)) ? 1 : 0.34;
                });
            };
            linkPaths
                .on('mouseenter', function (event, link) { applyHover(null, link); d3.select(this).raise(); })
                .on('mouseleave', () => applyHover());
            nodeG
                .on('mouseenter', function (event, node) { applyHover(node, null); d3.select(this).raise(); })
                .on('mouseleave', () => applyHover());

            svg.select('g.pc-legend').style('display', 'none').selectAll('*').remove();
        }

        function renderPaperlistTreemap(chartPayload) {
            const { parsed, compareParsed, allEntries, entries, currentKeys, compareKeys, zDomain, compareActive } = chartPayload;
            const activeCompare = !!(compareActive && compareKeys.length);
            setComparisonGlobals(activeCompare);

            const host = d3.select('#main-render');
            host.selectAll('div.pc-empty').remove();
            let svg = host.selectAll('svg.pc-chart-shared').data([1]);
            svg = svg.join('svg')
                .attr('class', 'pc-chart-shared')
                .attr('role', 'img');
            svg.interrupt();
            svg.attr('width', args.width)
                .attr('height', args.height)
                .attr('viewBox', [0, 0, args.width, args.height])
                .style('max-width', '100%')
                .style('height', 'auto');
            const svgNode = svg.node();
            if (!svgNode.__pc_hidden_tiers) svgNode.__pc_hidden_tiers = new Set();
            if (svgNode.__pc_paperlist_treemap_legend_folded == null) svgNode.__pc_paperlist_treemap_legend_folded = false;
            svgNode.__pc_active_chart = 'paperlist-treemap';
            svgNode.__pc_rerender = () => renderPaperlistTreemap(chartPayload);
            const hiddenTiers = svgNode.__pc_hidden_tiers;
            const legendFolded = !!svgNode.__pc_paperlist_treemap_legend_folded;
            const previousLayout = svgNode.__pc_paperlist_treemap_layout instanceof Map
                ? svgNode.__pc_paperlist_treemap_layout
                : new Map();
            const legendFoldTransition = svgNode.__pc_paperlist_treemap_last_folded != null
                && svgNode.__pc_paperlist_treemap_last_folded !== legendFolded;
            const treemapNodeKey = node => `${node && node.panel ? node.panel.side : 'cur'}|${node && node.data ? node.data.key : ''}`;
            const treemapNodeBox = node => ({
                x0: Math.max(0, Number(node.x0) || 0),
                y0: Math.max(0, Number(node.y0) || 0),
                x1: Math.max(0, Number(node.x1) || 0),
                y1: Math.max(0, Number(node.y1) || 0),
            });
            const previousNodeBox = node => previousLayout.get(treemapNodeKey(node));
            svg.selectAll('*').interrupt().remove();
            const defs = svg.append('defs');
            const clipBase = `pc-pl-treemap-clip-${Math.random().toString(36).slice(2, 9)}`;
            const applyCellClip = (g, node, suffix) => {
                const id = `${clipBase}-${suffix}`;
                const w = Math.max(0, node.x1 - node.x0);
                const h = Math.max(0, node.y1 - node.y0);
                const clip = defs.append('clipPath')
                    .attr('id', id)
                    .attr('clipPathUnits', 'userSpaceOnUse');
                clip.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', w)
                    .attr('height', h)
                    .attr('rx', 2)
                    .attr('ry', 2);
                g.selectAll('g.pc-paperlist-treemap-status-strip,g.pc-paperlist-treemap-inner,g.pc-paperlist-treemap-labels')
                    .attr('clip-path', `url(#${id})`);
            };

            const colorOrder = statusOrderForColors(zDomain);
            const tierColorMap = typeof window.pcTierColorMap === 'function'
                ? window.pcTierColorMap(colorOrder, zDomain)
                : Object.fromEntries(zDomain.map(status => [status, colorFor(status, zDomain)]));
            const fillForStatus = (status) => tierColorMap[status] || colorFor(status, zDomain);
            const acceptanceFillScale = d3.scaleLinear()
                .domain([0, 0.25, 0.5])
                .range(['#b91c1c', '#fef3c7', '#15803d'])
                .clamp(true);
            const tileFill = (d) => {
                if (d && d.isLegend) return '#f8fafc';
                return Number.isFinite(d.acceptance_rate) ? acceptanceFillScale(d.acceptance_rate) : '#e5e7eb';
            };
            const allCurrentEntries = sideEntries(allEntries, 'current');
            const allCompareEntries = sideEntries(allEntries, 'compare');
            const currentEntries = sideEntries(entries, 'current');
            const compareEntries = sideEntries(entries, 'compare');
            const currentTotal = treemapTotal(allCurrentEntries, currentKeys, zDomain, parsed, hiddenTiers);
            const compareTotal = activeCompare ? treemapTotal(allCompareEntries, compareKeys, zDomain, compareParsed, hiddenTiers) : 0;
            const currentRows = treemapRows(currentEntries, currentKeys, zDomain, parsed, hiddenTiers, currentTotal, currentDataset);
            const compareRows = activeCompare ? treemapRows(compareEntries, compareKeys, zDomain, compareParsed, hiddenTiers, compareTotal, compareDataset) : [];
            const comparisonPanelsActive = !!(activeCompare && compareRows.length);
            const standaloneLegendSpec = treemapStandaloneLegendSpec(comparisonPanelsActive, zDomain.length, legendFolded);
            if (!currentRows.length && !compareRows.length) {
                showEmpty('No treemap data available for this paperlist metric.');
                return;
            }

            const body = svg.append('g').attr('class', 'pc-body-paperlist-treemap');
            const panels = treemapPanels(
                currentRows,
                compareRows,
                comparisonPanelsActive,
                currentTotal,
                compareTotal,
                standaloneLegendSpec ? standaloneLegendSpec.reserveW : 0
            );
            const duration = args.animate ? (legendFoldTransition ? 760 : 520) : 0;
            const layoutEase = legendFoldTransition ? d3.easeCubicInOut : d3.easeCubicOut;
            const panelNodes = [];
            panels.forEach(panel => {
                body.append('rect')
                    .attr('class', `pc-paperlist-treemap-panel pc-paperlist-treemap-panel-${panel.side}`)
                    .attr('x', panel.x)
                    .attr('y', panel.y)
                    .attr('width', Math.max(0, panel.w))
                    .attr('height', Math.max(0, panel.h))
                    .attr('fill', 'none')
                    .attr('stroke', panel.side === 'cmp' ? '#10b981' : '#4062BB')
                    .attr('stroke-opacity', activeCompare ? 0.45 : 0.16)
                    .attr('stroke-width', activeCompare ? 1.4 : 1);
                body.append('text')
                    .attr('class', 'pc-paperlist-treemap-panel-label')
                    .attr('x', panel.x + 2)
                    .attr('y', panel.y - 10)
                    .attr('font-size', 13)
                    .attr('font-weight', 800)
                    .attr('fill', panel.side === 'cmp' ? '#065f46' : '#1e3a8a')
                    .text(panel.label);
                if (!panel.rows.length || panel.w < 12 || panel.h < 12) return;
                const includeLegend = !standaloneLegendSpec && panel.side === 'cur' && zDomain.length;
                const layoutRows = includeLegend
                    ? panel.rows.concat([treemapLegendDatum(treemapLegendValue(panel.rows, activeCompare, zDomain.length, panel, legendFolded))])
                    : panel.rows;
                const root = d3.hierarchy({ children: layoutRows })
                    .sum(d => d.value)
                    .sort(treemapNodeSort);
                d3.treemap()
                    .tile(d3.treemapSquarify.ratio(1.12))
                    .size([Math.max(1, panel.w), Math.max(1, panel.h)])
                    .paddingInner(2)
                    .round(true)(root);
                root.leaves().forEach(node => {
                    node.x0 += panel.x;
                    node.x1 += panel.x;
                    node.y0 += panel.y;
                    node.y1 += panel.y;
                    node.panel = panel;
                    panelNodes.push(node);
                });
            });
            const innerScale = {
                groupedStatuses: zDomain.filter(status => !hiddenTiers.has(status)),
                pieMaxValue: Math.max(1, d3.max(panelNodes, node => {
                    if (!node || !node.data || node.data.isLegend) return 0;
                    return Number(node.data.value) || 0;
                }) || 1),
                groupedMax: Math.max(1, d3.max(panelNodes, node => {
                    if (!node || !node.data || node.data.isLegend) return 0;
                    return d3.max(node.data.statusSegments || [], seg => Number(seg.count) || 0) || 0;
                }) || 1),
            };
            if (!innerScale.groupedStatuses.length) innerScale.groupedStatuses = zDomain.slice();

            const popup = body.append('g')
                .attr('class', 'pc-paperlist-treemap-popup pc-dot-popup')
                .style('display', 'none')
                .style('pointer-events', 'none');
            popup.append('rect')
                .attr('class', 'pc-paperlist-treemap-popup-bg pc-dot-bg')
                .attr('rx', 5)
                .attr('ry', 5)
                .attr('fill', 'rgba(255,255,255,0.94)')
                .attr('stroke', 'rgba(15,23,42,0.16)');
            for (let i = 0; i < 20; i++) {
                popup.append('text')
                    .attr('class', `pc-dot-text pc-paperlist-treemap-popup-text pc-dot-line-${i}`)
                    .attr('text-anchor', 'start')
                    .attr('font-size', 12)
                    .attr('fill', '#333');
            }

            const showPopup = (event, node, activeStatus = null) => {
                const d = node.data;
                const total = Math.max(1, Number(node.panel.total) || d3.sum(node.panel.rows, row => row.value) || 1);
                const sharedCountText = (count) => typeof pcPopupCountText === 'function' ? pcPopupCountText(count) : formatCount(count);
                const sharedPct = (ratio) => typeof pcPopupPct === 'function'
                    ? pcPopupPct((Number(ratio) || 0) * 100)
                    : d3.format('.1%')(Number(ratio) || 0);
                const tableLine = (cells, widths, fill = '#333', style = 'table') => ({
                    text: cells.join(' '),
                    cells,
                    widths,
                    fill,
                    style,
                });
                const lines = [
                    { text: d.label, fill: '#111827', style: 'title' },
                    { text: 'Summary', fill: '#64748b', style: 'section' },
                    tableLine(['Metric', 'Value'], [92, 86], '#64748b', 'tableHeader'),
                    tableLine(['Count', sharedCountText(d.value)], [92, 86], '#334155'),
                    tableLine(['Panel share', sharedPct(d.value / total)], [92, 86], '#334155'),
                    tableLine(['Acceptance', Number.isFinite(d.acceptance_rate) ? sharedPct(d.acceptance_rate) : '-'], [92, 86], '#334155'),
                ];
                if (d.statusSegments.length) {
                    lines.push({ text: 'Tiers', fill: '#64748b', style: 'section' });
                    if (typeof pcPopupBivarStatsHeader === 'function') {
                        lines.push(pcPopupBivarStatsHeader('#64748b'));
                    } else {
                        lines.push(tableLine(['Scope', 'Count', 'Percentage'], [56, 70, 92], '#64748b', 'tableHeader'));
                    }
                    d.statusSegments.forEach(seg => {
                        const isActiveTier = activeStatus && seg.status === activeStatus;
                        if (typeof pcPopupBivarStatsLine === 'function') {
                            const line = pcPopupBivarStatsLine(
                                seg.status,
                                seg.count,
                                Math.max(1, d.statusSegmentTotal || d.value),
                                fillForStatus(seg.status)
                            );
                            if (isActiveTier) line.style = 'tableActive';
                            lines.push(line);
                        } else {
                            lines.push(tableLine(
                                [seg.status, sharedCountText(seg.count), sharedPct(seg.count / Math.max(1, d.statusSegmentTotal || d.value))],
                                [56, 70, 92],
                                fillForStatus(seg.status),
                                isActiveTier ? 'tableActive' : 'table'
                            ));
                        }
                    });
                }
                let popupW;
                let popupH;
                if (typeof pcLayoutPopupRows === 'function') {
                    ({ popupW, popupH } = pcLayoutPopupRows(popup, lines, { padH: 8, padV: 6, colGap: 14 }));
                } else {
                    const text = popup.selectAll('text.pc-dot-text').data(lines);
                    text.exit().remove();
                    text.enter().append('text')
                        .attr('class', 'pc-dot-text pc-paperlist-treemap-popup-text')
                        .attr('x', 10)
                      .merge(text)
                        .attr('x', 10)
                        .attr('y', (_, i) => 17 + i * 17)
                        .attr('font-size', 12)
                        .attr('font-weight', line => line.style === 'title' ? 800 : 500)
                        .attr('fill', line => line.fill || '#334155')
                        .text(line => line.text || '');
                    popupW = Math.max(180, Math.min(340, d3.max(lines, line => String(line.text || '').length) * 6.6 + 22));
                    popupH = 20 + lines.length * 17;
                }
                const point = d3.pointer(event, svg.node());
                let x = point[0] + 12;
                let y = point[1] - popupH - 12;
                if (x + popupW > args.width - 8) x = point[0] - popupW - 12;
                if (y < 8) y = point[1] + 12;
                popup.attr('transform', `translate(${x},${y})`).style('display', null).raise();
                popup.select('rect.pc-paperlist-treemap-popup-bg').attr('width', popupW).attr('height', popupH);
            };
            const hidePopup = () => {
                popup.style('display', 'none');
                body.selectAll('rect.pc-paperlist-treemap-rect')
                    .classed('pc-paperlist-treemap-highlight', false);
                resetInnerComponentHighlight();
            };
            const innerBaseOpacity = function () {
                if (this.classList && this.classList.contains('pc-paperlist-treemap-inner-bar')) return 0.88;
                if (this.classList && this.classList.contains('pc-paperlist-treemap-inner-strip')) return 0.94;
                return 0.92;
            };
            const resetInnerComponentHighlight = () => {
                body.selectAll('.pc-paperlist-treemap-inner-mark')
                    .interrupt('pc-paperlist-inner-highlight')
                    .classed('pc-paperlist-treemap-inner-highlight', false)
                    .transition('pc-paperlist-inner-highlight')
                    .duration(90)
                    .attr('opacity', innerBaseOpacity);
            };
            const highlightInnerComponent = (status) => {
                if (!status) return;
                body.selectAll('.pc-paperlist-treemap-inner-mark')
                    .interrupt('pc-paperlist-inner-highlight')
                    .classed('pc-paperlist-treemap-inner-highlight', function () {
                        return this.getAttribute('data-status') === status;
                    })
                    .transition('pc-paperlist-inner-highlight')
                    .duration(90)
                    .attr('opacity', function () {
                        return this.getAttribute('data-status') === status ? 0.96 : 0.48;
                    });
                body.selectAll('.pc-paperlist-treemap-inner-mark')
                    .filter(function () { return this.getAttribute('data-status') === status; })
                    .raise();
            };

            const cells = body.selectAll('g.pc-paperlist-treemap-cell')
                .data(panelNodes, treemapNodeKey)
                .join(enter => {
                    const g = enter.append('g')
                        .attr('class', 'pc-paperlist-treemap-cell')
                        .attr('transform', node => {
                            const prev = previousNodeBox(node);
                            return prev ? `translate(${prev.x0},${prev.y0})` : `translate(${node.x0},${node.y0})`;
                        })
                        .style('cursor', 'default');
                    g.append('rect')
                        .attr('class', 'pc-paperlist-treemap-rect')
                        .attr('rx', 2)
                        .attr('ry', 2)
                        .attr('width', node => {
                            const prev = previousNodeBox(node);
                            return prev ? Math.max(0, prev.x1 - prev.x0) : 0;
                        })
                        .attr('height', node => {
                            const prev = previousNodeBox(node);
                            return prev ? Math.max(0, prev.y1 - prev.y0) : 0;
                        });
                    g.append('g').attr('class', 'pc-paperlist-treemap-status-strip');
                    g.append('g').attr('class', 'pc-paperlist-treemap-inner');
                    g.append('g').attr('class', 'pc-paperlist-treemap-labels');
                    return g;
                });
            cells
                .on('mouseenter', function (event, node) {
                    if (node.data && node.data.isLegend) {
                        hidePopup();
                        return;
                    }
                    body.selectAll('rect.pc-paperlist-treemap-rect').classed('pc-paperlist-treemap-highlight', false);
                    d3.select(this).select('rect.pc-paperlist-treemap-rect').classed('pc-paperlist-treemap-highlight', true);
                    showPopup(event, node);
                })
                .on('mousemove', function (event, node) {
                    if (node.data && node.data.isLegend) return;
                    showPopup(event, node);
                })
                .on('mouseleave', hidePopup);
            cells.transition().duration(duration).ease(layoutEase)
                .attr('transform', node => `translate(${node.x0},${node.y0})`);
            cells.select('rect.pc-paperlist-treemap-rect')
                .transition().duration(duration).ease(layoutEase)
                .attr('width', node => Math.max(0, node.x1 - node.x0))
                .attr('height', node => Math.max(0, node.y1 - node.y0))
                .attr('fill', node => tileFill(node.data))
                .attr('stroke', node => node.data && node.data.isLegend ? 'rgba(100,116,139,0.55)' : 'rgba(255,255,255,0.92)')
                .attr('stroke-width', 1);

            cells.each(function (node, i) {
                const g = d3.select(this);
                const d = node.data;
                applyCellClip(g, node, i);
                if (d && d.isLegend) {
                    drawPaperlistTreemapLegendCell(g, node, zDomain, hiddenTiers, fillForStatus, chartPayload, acceptanceFillScale, body, svgNode);
                    return;
                }
                const w = Math.max(0, node.x1 - node.x0);
                const h = Math.max(0, node.y1 - node.y0);
                const strip = g.select('g.pc-paperlist-treemap-status-strip');
                strip.selectAll('*').remove();
                let innerH = drawPaperlistTileChart(g, node, fillForStatus, innerScale);
                const tileMode = TILE_CHART_TYPES.includes(args.tileChart) ? args.tileChart : 'Status pie';
                const hasPie = !g.select('g.pc-paperlist-treemap-inner-pie').empty();

                const labelG = g.select('g.pc-paperlist-treemap-labels');
                labelG.selectAll('*').remove();
                let labelAvailH = Math.max(0, h - (hasPie ? 0 : innerH) - 8);
                if (w < 28 || labelAvailH < 12) return;
                const fill = readableTextColor(tileFill(d));
                const stroke = fill === '#fff' ? 'rgba(15,23,42,0.38)' : 'rgba(255,255,255,0.72)';
                const fs = Math.max(8, Math.min(16, Math.sqrt(w * h) / 16));
                const countFs = Math.max(8, Math.min(12, fs - 3));
                const titleY = 7 + fs * 0.95;
                const countY = titleY + Math.max(11, countFs + 3);
                let showCountLine = w >= 42 && labelAvailH >= countY + 2;
                if (!showCountLine && tileMode !== 'Status pie' && innerH > 0 && w >= 42 && h >= countY + 8) {
                    g.select('g.pc-paperlist-treemap-inner').selectAll('*').remove();
                    g.select('g.pc-paperlist-treemap-status-strip').selectAll('*').remove();
                    innerH = 0;
                    labelAvailH = Math.max(0, h - 8);
                    showCountLine = labelAvailH >= countY + 2;
                }
                const maxChars = Math.max(5, Math.floor((w - 10) / (fs * 0.56)));
                const lines = wrappedWords(d.label, maxChars, showCountLine ? 1 : (labelAvailH >= 54 ? 2 : 1));
                lines.forEach((line, lineIdx) => {
                    labelG.append('text')
                        .attr('x', 7)
                        .attr('y', titleY + fs * lineIdx)
                        .attr('font-size', fs)
                        .attr('font-weight', 800)
                        .attr('fill', fill)
                        .attr('paint-order', 'stroke')
                        .attr('stroke', stroke)
                        .attr('stroke-width', 2.2)
                        .attr('stroke-linejoin', 'round')
                        .text(line);
                });
                if (showCountLine) {
                    const acceptText = Number.isFinite(d.acceptance_rate)
                        ? `acc ${d3.format('.1%')(d.acceptance_rate)}`
                        : 'acc -';
                    const countText = w >= 86
                        ? `${formatCount(d.value)} · ${acceptText}`
                        : acceptText;
                    labelG.append('text')
                        .attr('x', 7)
                        .attr('y', Math.min(labelAvailH - 2, countY))
                        .attr('font-size', countFs)
                        .attr('font-weight', 750)
                        .attr('fill', fill)
                        .attr('paint-order', 'stroke')
                        .attr('stroke', stroke)
                        .attr('stroke-width', 1.8)
                        .text(countText);
                }
                if (duration && legendFoldTransition && previousNodeBox(node)) {
                    g.selectAll('g.pc-paperlist-treemap-status-strip,g.pc-paperlist-treemap-inner,g.pc-paperlist-treemap-labels')
                        .attr('opacity', 0.62)
                        .transition().duration(Math.min(260, duration)).delay(Math.max(0, duration - 280))
                        .attr('opacity', 1);
                }
            });
            cells.filter(node => node.data && node.data.isLegend).raise();
            body.select('g.pc-paperlist-notes-popup').raise();

            const standaloneLegendNode = treemapStandaloneLegendNode(standaloneLegendSpec);
            if (standaloneLegendNode) {
                const prevStandalone = previousNodeBox(standaloneLegendNode);
                const legendG = body.append('g')
                    .datum(standaloneLegendNode)
                    .attr('class', 'pc-paperlist-treemap-cell pc-paperlist-treemap-legend-standalone')
                    .attr('transform', prevStandalone
                        ? `translate(${prevStandalone.x0},${prevStandalone.y0})`
                        : `translate(${standaloneLegendNode.x0},${standaloneLegendNode.y0})`)
                    .style('cursor', 'default');
                legendG.append('rect')
                    .attr('class', 'pc-paperlist-treemap-rect')
                    .attr('rx', 2)
                    .attr('ry', 2)
                    .attr('width', prevStandalone ? Math.max(0, prevStandalone.x1 - prevStandalone.x0) : 0)
                    .attr('height', prevStandalone ? Math.max(0, prevStandalone.y1 - prevStandalone.y0) : 0)
                    .attr('fill', tileFill(standaloneLegendNode.data))
                    .attr('stroke', 'rgba(100,116,139,0.55)')
                    .attr('stroke-width', 1);
                legendG.append('g').attr('class', 'pc-paperlist-treemap-status-strip');
                legendG.append('g').attr('class', 'pc-paperlist-treemap-inner');
                legendG.append('g').attr('class', 'pc-paperlist-treemap-labels');
                applyCellClip(legendG, standaloneLegendNode, 'standalone-legend');
                drawPaperlistTreemapLegendCell(legendG, standaloneLegendNode, zDomain, hiddenTiers, fillForStatus, chartPayload, acceptanceFillScale, body, svgNode);
                legendG.transition().duration(duration).ease(layoutEase)
                    .attr('transform', `translate(${standaloneLegendNode.x0},${standaloneLegendNode.y0})`);
                legendG.select('rect.pc-paperlist-treemap-rect')
                    .transition().duration(duration).ease(layoutEase)
                    .attr('width', Math.max(0, standaloneLegendNode.x1 - standaloneLegendNode.x0))
                    .attr('height', Math.max(0, standaloneLegendNode.y1 - standaloneLegendNode.y0));
            }

            body.selectAll('text.pc-paperlist-treemap-panel-label').raise();

            body.selectAll('.pc-paperlist-treemap-inner-mark')
                .attr('pointer-events', 'all')
                .style('pointer-events', 'all')
                .style('cursor', 'default')
                .on('mouseenter.pc-paperlist-inner mousemove.pc-paperlist-inner', function (event) {
                    if (event && event.stopPropagation) event.stopPropagation();
                    const status = this.getAttribute('data-status');
                    highlightInnerComponent(status);
                    const cell = this.closest && this.closest('g.pc-paperlist-treemap-cell');
                    const node = cell ? d3.select(cell).datum() : null;
                    if (node && node.data && !node.data.isLegend) {
                        body.selectAll('rect.pc-paperlist-treemap-rect').classed('pc-paperlist-treemap-highlight', false);
                        d3.select(cell).select('rect.pc-paperlist-treemap-rect').classed('pc-paperlist-treemap-highlight', true);
                        showPopup(event, node, status);
                    }
                })
                .on('mouseleave.pc-paperlist-inner', resetInnerComponentHighlight);

            const nextLayout = new Map();
            panelNodes.forEach(node => {
                nextLayout.set(treemapNodeKey(node), treemapNodeBox(node));
            });
            if (standaloneLegendNode) {
                nextLayout.set(treemapNodeKey(standaloneLegendNode), treemapNodeBox(standaloneLegendNode));
            }
            svgNode.__pc_paperlist_treemap_layout = nextLayout;
            svgNode.__pc_paperlist_treemap_last_folded = legendFolded;

            svg.select('g.pc-legend').style('display', 'none').selectAll('*').remove();
        }

        function injectStyle() {
            if (document.getElementById('pc-paperlist-style')) return;
            const css = `
                .pc-paperlist-visual { margin:8px 0 22px; }
                #main-render { display:flex; justify-content:center; width:100%; aspect-ratio:1400 / 600; overflow:hidden; }
                #main-render svg.pc-chart-shared { display:block; width:100%; height:auto; }
                @keyframes pc-paperlist-treemap-breathe {
                    0%, 100% { stroke-opacity:0.56; stroke-width:1.8; }
                    50% { stroke-opacity:1; stroke-width:3.4; }
                }
                @keyframes pc-paperlist-treemap-inner-breathe {
                    0%, 100% { stroke-opacity:0.32; stroke-width:0.8; }
                    50% { stroke-opacity:0.72; stroke-width:1.5; }
                }
                .pc-paperlist-treemap-highlight {
                    stroke:#111827 !important;
                    vector-effect:non-scaling-stroke;
                    animation:pc-paperlist-treemap-breathe 1.4s ease-in-out infinite;
                }
                .pc-paperlist-treemap-inner-highlight {
                    stroke:#334155 !important;
                    vector-effect:non-scaling-stroke;
                    animation:pc-paperlist-treemap-inner-breathe 1.8s ease-in-out infinite;
                }
                #pc_controls { display:flex; flex-direction:column; gap:10px; padding:12px 6px; margin:4px 0 10px;
                    font-size:14px; border-top:1px solid #eee; border-bottom:1px solid #eee; }
                #pc_controls .pc_row { display:flex; flex-wrap:wrap; gap:10px; align-items:center; }
                #pc_controls .pc_row_label { font-weight:600; white-space:nowrap; }
                #pc_controls #pc_status_row { justify-content:flex-start; background:#f3f5f9; border-radius:6px; padding:10px 12px; margin:0 -6px; gap:8px; }
                #pc_controls #pc_status_row .pc_status_btn { flex:1 1 0; min-width:160px; max-width:none; text-align:center; }
                #pc_controls .pc_status_btn { font-size:13px; padding:8px 14px; border:1px solid #b8bec7;
                    background:#fafbfc; color:#222; border-radius:6px; cursor:pointer; line-height:1.2;
                    font-weight:500; transition:all 120ms ease;
                    display:inline-flex; flex-direction:column; align-items:center; justify-content:center; gap:2px; }
                #pc_controls .pc_status_btn .pc_status_label { font-size:13px; font-weight:600; line-height:1.15; position:relative; }
                #pc_controls .pc_status_btn .pc_status_desc { font-size:11px; font-weight:400; line-height:1.1; color:#6b7280; }
                #pc_controls .pc_status_btn:hover { border-color:#4062BB; color:#4062BB; background:#fff; }
                #pc_controls .pc_status_btn.active { background:#4062BB; border-color:#4062BB; color:#fff; font-weight:600; box-shadow:0 2px 5px rgba(64,98,187,0.25); }
                #pc_controls .pc_status_btn.active .pc_status_desc { color:#dde5fa; }
                #pc_controls .pc_view_wrap { position:relative; flex:1 1 0; min-width:160px; min-height:58px; }
                #pc_controls .pc_phase_row, #pc_controls .pc_cmp_row { display:flex; gap:3px; width:100%; margin-top:2px; align-items:stretch; }
                #pc_controls .pc_phase_pill { flex:1; font-family:inherit; font-size:10px; font-weight:500; padding:3px 4px;
                    border:1px solid transparent; border-radius:3px; background:rgba(0,0,0,0.04); color:inherit;
                    cursor:pointer; line-height:1.1; min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
                #pc_controls .pc_phase_pill.active { background:#fff; color:#4062BB; font-weight:700; border-color:#fff; }
                #pc_controls .pc_view_wrap.active .pc_phase_pill { background:rgba(255,255,255,0.18); color:#fff; }
                #pc_controls .pc_view_wrap.active .pc_phase_pill.active { background:#fff; color:#4062BB; }
                #pc_controls .pc_cmp_field { flex:1 1 0; min-width:0; display:flex; align-items:center; gap:4px; margin:0; cursor:pointer; }
                #pc_controls .pc_cmp_label { font-size:9px; font-weight:600; letter-spacing:0.06em; text-transform:uppercase;
                    opacity:0.7; user-select:none; flex-shrink:0; line-height:1; white-space:nowrap; }
                #pc_controls .pc_cmp_select { flex:1 1 0 !important; min-width:0 !important; font-family:inherit !important;
                    font-size:10px !important; font-weight:500 !important; height:20px !important; min-height:20px !important;
                    max-height:20px !important; line-height:1.1 !important; box-sizing:border-box !important;
                    padding:0 14px 0 5px !important; margin:0 !important; border:1px solid transparent !important;
                    border-radius:3px !important; background-color:rgba(0,0,0,0.04) !important; color:inherit !important;
                    cursor:pointer !important; appearance:none !important;
                    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 24 24'><path fill='%23666' d='M7 10l5 5 5-5z'/></svg>") !important;
                    background-repeat:no-repeat !important; background-position:right 3px center !important; background-size:8px !important; }
                #pc_controls .pc_view_wrap[data-view="Comparison"] .pc_cmp_hint { position:absolute; left:100%; top:50%;
                    transform:translateY(-50%); margin-left:6px; font-size:9px; font-weight:600; letter-spacing:0.06em;
                    text-transform:uppercase; opacity:0.75; user-select:none; white-space:nowrap; color:#0f9d6f; transition:opacity 0.2s ease; }
                #pc_controls .pc_view_wrap.active[data-view="Comparison"] { background:#10b981 !important; border-color:#0f9d6f !important;
                    color:#fff !important; box-shadow:0 2px 5px rgba(16,185,129,0.25) !important; }
                #pc_controls .pc_view_wrap.active[data-view="Comparison"] .pc_cmp_hint { opacity:0; }
                #pc_controls .pc_view_wrap.active[data-view="Comparison"] .pc_cmp_select,
                #pc_controls .pc_view_wrap.active .pc_cmp_select { background-color:rgba(255,255,255,0.18) !important; color:#fff !important;
                    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 24 24'><path fill='%23fff' d='M7 10l5 5 5-5z'/></svg>") !important; }
                #pc_controls .pc_view_wrap.active .pc_cmp_select option { color:#222; }
                #pc_controls #pc_row2 { flex-wrap:nowrap; gap:10px; }
                #pc_controls #pc_row2 > * { flex:1 1 0; min-width:0; }
                #pc_controls #pc_row2 > label.pc_display_cap_field { flex:1.45 1 230px; min-width:220px; }
                #pc_controls #pc_row2 > #pc_btn_settings { flex:0 0 auto; min-width:132px; white-space:nowrap; }
                #pc_controls #pc_row2 label { display:flex; gap:6px; align-items:center; min-width:0; margin:0; }
                #pc_controls #pc_row2 label select, #pc_controls #pc_row2 .pc_action,
                #pc_controls #pc_row2 input[type="number"] { height:36px !important; min-height:36px !important; max-height:36px !important;
                    box-sizing:border-box !important; font-size:13px !important; font-family:inherit !important; line-height:1 !important;
                    margin:0 !important; color:#333; border:1px solid #c8cdd4 !important; border-radius:4px !important;
                    background-color:#fff !important; }
                #pc_controls #pc_row2 label select { flex:1; min-width:0; padding:0 28px 0 10px; cursor:pointer; appearance:none !important;
                    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'><path fill='%23666' d='M7 10l5 5 5-5z'/></svg>");
                    background-repeat:no-repeat; background-position:right 8px center; background-size:12px; }
                #pc_controls #pc_row2 input[type="number"] { width:72px; padding:0 8px; }
                #pc_controls #pc_row2 input[type="range"] { flex:1; min-width:90px; accent-color:#4062BB; }
                #pc_controls .pc_action { justify-content:center !important; text-align:center; padding:0 12px; cursor:pointer;
                    display:inline-flex !important; align-items:center !important; gap:6px; transition:all 120ms ease; }
                #pc_controls .pc_action_gear { transform-origin:50% 50%; transition:transform 600ms ease; }
                #pc_controls button.pc_action:hover .pc_action_gear,
                #pc_controls button.pc_action.pc-gear-hover .pc_action_gear { transform:rotate(120deg); }
                #pc_controls #pc_row2 label select:hover, #pc_controls #pc_row2 .pc_action:hover { border-color:#4062BB !important; color:#4062BB; background-color:#f6f7fa !important; }
                #pc_controls #pc_row2 .pc_action.active { background-color:#eef3fd !important; border-color:#4062BB !important; color:#4062BB !important; font-weight:600 !important; }
                #gui { display:none; flex-wrap:wrap; align-items:center; gap:10px; padding:10px 12px; background:#fafbfc;
                    border:1px solid #e1e5ec; border-radius:6px; margin-top:2px; }
                #gui label { display:flex; align-items:center; gap:6px; margin:0; font-size:12px; font-weight:600; color:#333; }
                #gui input[type="number"] { width:86px; height:30px; min-height:30px; border:1px solid #c8cdd4; border-radius:4px; padding:0 8px; }
                #gui input[type="checkbox"] { accent-color:#4062BB; }
                #paperlist { border-collapse:separate; border-spacing:0; width:100%; }
                #paperlist thead th { position:sticky; top:0; z-index:2; background:#f7f8fb; border-bottom:1px solid #d9dee8; }
                #paperlist input { min-height:28px; border:1px solid #c8ced8; border-radius:5px; padding:2px 6px; font-size:12px; }
                #paperlist .sort-btn, #btn_fetchall, #btn_hide_reject { border-radius:5px; font-size:12px; text-decoration:none; cursor:pointer; }
                @media (max-width: 780px) {
                    #pc_controls #pc_row2 { flex-wrap:wrap; }
                    #pc_controls #pc_row2 > * { flex-basis:100%; }
                    #main-render { aspect-ratio:1400 / 1000; }
                }
            `;
            document.head.appendChild(Object.assign(document.createElement('style'), { id: 'pc-paperlist-style', textContent: css }));
        }

        function buildShell() {
            injectStyle();
            const axisOptions = axisOptionsHtml();
            const phasePills = STATUS_VIEWS
                .map(opt => `<button type="button" class="pc_phase_pill" data-val="${esc(opt.value)}" title="${esc(opt.desc)}">${esc(opt.label)}</button>`)
                .join('');
            const chartOptions = chartOptionsHtml();
            const tileChartOptions = TILE_CHART_TYPES
                .map(opt => `<option value="${esc(opt)}">${esc(opt)}</option>`)
                .join('');
            const shell = `
                <section class="pc-paperlist-visual">
                    <div id="main-render"></div>
                    <div id="pc_controls">
                        <div class="pc_row" id="pc_status_row">
                            <span class="pc_row_label">View:</span>
                            <div class="pc_view_wrap pc_status_btn active" role="button" tabindex="0" data-view="Phase" title="Choose paperlist status view">
                                <span class="pc_status_label">Phase</span>
                                <div class="pc_phase_row">${phasePills}</div>
                            </div>
                            <div class="pc_view_wrap pc_status_btn" role="button" tabindex="0" data-view="Comparison" title="Compare against another venue and year">
                                <span class="pc_status_label">Comparison<span class="pc_cmp_hint">&larr; click to enable</span></span>
                                <div class="pc_cmp_row">
                                    <label class="pc_cmp_field"><span class="pc_cmp_label">Venue</span><select id="pc_cmp_venue" class="pc_cmp_select" title="Compare venue"><option value="">Venue&hellip;</option></select></label>
                                    <label class="pc_cmp_field"><span class="pc_cmp_label">Year</span><select id="pc_cmp_year" class="pc_cmp_select" title="Compare year" disabled><option value="">Year&hellip;</option></select></label>
                                    <label class="pc_cmp_field"><span class="pc_cmp_label">Mode</span><select id="pc_cmp_mode" class="pc_cmp_select"><option value="normalized">Normalized</option><option value="proportional">Proportional</option></select></label>
                                    <label class="pc_cmp_field"><span class="pc_cmp_label">Layout</span><select id="pc_cmp_merge" class="pc_cmp_select"><option value="split_h">Split H</option><option value="sbs_h">Side H</option><option value="split_v">Split V</option><option value="sbs_v">Side V</option></select></label>
                                </div>
                            </div>
                        </div>
                        <div class="pc_row" id="pc_row2">
                            <label><span class="pc_row_label">Chart</span><select id="pc_chart_select">${chartOptions}</select></label>
                            <label id="pc_pl_tile_label" style="display:none"><span class="pc_row_label">Tile Chart</span><select id="pc_pl_tile_chart">${tileChartOptions}</select></label>
                            <label><span class="pc_row_label">Metric</span><select id="pc_pl_axis">${axisOptions}</select></label>
                            <label class="pc_display_cap_field"><span class="pc_row_label">Display Cap</span><input id="pc_pl_top_range" type="range" min="10" step="1"><input id="pc_pl_top_number" type="number" min="1" step="1"></label>
                            <button type="button" class="pc_action" id="pc_btn_settings" title="Advanced settings">${PC_PAPERLIST_GEAR_SVG}<span>Settings [S]</span></button>
                        </div>
                        <div id="gui">
                            <label>Width <input id="pc_pl_width" type="number" min="400" max="3000" step="50"></label>
                            <label>Height <input id="pc_pl_height" type="number" min="260" max="1600" step="20"></label>
                            <label><input id="pc_pl_labels" type="checkbox"> Axis labels</label>
                            <label><input id="pc_pl_animate" type="checkbox"> Animate</label>
                        </div>
                    </div>
                </section>`;
            const target = $('#main');
            let existing = $();
            if (target.length) {
                existing = target.find('section.pc-paperlist-visual.pc-chart-first-placeholder').first();
                if (!existing.length) existing = target.children('.pc-paperlist-visual').first();
                if (!existing.length) existing = target.find('section.pc-paperlist-visual').first();
            } else {
                existing = $('body').children('.pc-paperlist-visual').first();
            }
            if (existing.length) existing.replaceWith(shell);
            else if (target.length) target.prepend(shell);
            else $('body').prepend(shell);
        }

        function syncControls() {
            const topMax = args.chart === 'Flow' ? TOP_CAP : topLimit();
            if (args.numBars > topMax) args.numBars = topMax;
            const topRangeMin = Math.min(10, topMax);
            const visibleTop = Math.min(args.numBars, topMax);
            $('#pc_chart_select').val(args.chart);
            $('#pc_pl_tile_label').toggle(args.chart === 'Treemap');
            if (!TILE_CHART_TYPES.includes(args.tileChart)) args.tileChart = 'Status pie';
            $('#pc_pl_tile_chart').val(args.tileChart);
            $('#pc_pl_axis').val(args.xaxis);
            $('#pc_pl_axis').closest('label').toggle(args.chart !== 'Flow');
            $('#pc_pl_top_range').attr('min', topRangeMin).attr('max', topMax).val(visibleTop);
            $('#pc_pl_top_number').attr('max', topMax).val(visibleTop);
            $('#pc_pl_width').val(args.width);
            $('#pc_pl_height').val(args.height);
            $('#pc_pl_labels').prop('checked', args.showLabels);
            $('#pc_pl_labels').closest('label').toggle(args.chart !== 'Treemap' && args.chart !== 'Flow');
            $('#pc_pl_animate').prop('checked', args.animate);
            $('#pc_cmp_venue').val(args.comparison.conf || '');
            $('#pc_cmp_year').val(args.comparison.year || '');
            $('#pc_cmp_mode').val(args.comparison.mode);
            $('#pc_cmp_merge').val(args.comparison.layout);
            $('.pc_view_wrap[data-view="Phase"]').addClass('active');
            $('.pc_view_wrap[data-view="Comparison"]').toggleClass('active', args.comparison.active);
            $('.pc_phase_pill').each(function () {
                $(this).toggleClass('active', this.dataset.val === args.view);
            });
            $('#main-render').toggleClass('pc-comparison-on', args.comparison.active);
        }

        function showEmpty(message) {
            const host = d3.select('#main-render');
            host.selectAll('*').remove();
            host.append('div')
                .attr('class', 'pc-empty')
                .style('padding', '60px 20px')
                .style('color', '#777')
                .style('text-align', 'center')
                .text(message);
        }

        function renderChart() {
            if (args.chart === 'Flow' && args.comparison.active) args.comparison.active = false;
            syncControls();
            if (args.chart === 'Flow') {
                const flowPayload = ensureFlowDataset(() => renderChart());
                if (!flowPayload) {
                    const host = d3.select('#main-render');
                    if (host.select('svg.pc-chart-shared g.pc-body-paperlist-flow').empty()) {
                        showEmpty(flowError || 'Loading relationship data...');
                    }
                    return;
                }
                renderPaperlistFlowChart(flowPayload);
                return;
            }
            if (args.comparison.active) {
                ensureCompareDataset(() => renderChart());
            }
            const chartPayload = buildChartData();
            const { parsed, entries, data, compareBins, zDomain, compareActive } = chartPayload;
            if (!entries.length || !zDomain.length || !data.length) {
                showEmpty('No chart data available for this paperlist metric.');
                return;
            }
            if (args.chart === 'Treemap') {
                renderPaperlistTreemap(chartPayload);
                return;
            }
            const sharedChart = window.pcSharedBarChartTransition;
            if (typeof sharedChart !== 'function') {
                showEmpty('Shared statistics chart renderer is not available.');
                return;
            }
            const tick = tickSpec(entries);
            const host = d3.select('#main-render');
            host.select('svg.pc-chart-shared')
                .selectAll('g.pc-body-paperlist-treemap,g.pc-paperlist-treemap-legend,g.pc-legend')
                .interrupt()
                .remove();
            host.select('svg.pc-chart-shared defs')
                .selectAll('clipPath[id^="pc-pl-treemap-clip"]')
                .remove();
            const colorOrder = statusOrderForColors(zDomain);
            const tierColorMap = typeof window.pcTierColorMap === 'function'
                ? window.pcTierColorMap(colorOrder, zDomain)
                : Object.fromEntries(zDomain.map(status => [status, colorFor(status, zDomain)]));
            const colors = zDomain.map(status => tierColorMap[status] || colorFor(status, zDomain));
            setComparisonGlobals(compareActive);
            const linesOnly = args.chart === 'Line';
            sharedChart(data, {
                host,
                width: args.width,
                height: args.height,
                margin: { top: 62, right: 150, bottom: args.showLabels ? 150 : 64, left: 72 },
                zDomain,
                colors,
                tierColorMap,
                bar_mode: chartMode(),
                animation: args.animate,
                step_rating: 1,
                xLabel: args.showLabels ? axisLabel(args.xaxis) : `${axisLabel(args.xaxis)} rank`,
                yLabel: 'Count',
                y2Label: 'Percentage',
                line: args.line,
                merge_active: false,
                lines_only: linesOnly,
                compareBins: compareActive ? compareBins : null,
                compareMode: compareActive ? comparisonToken() : 'normalized_split_h',
                xTickValuesOverride: tick.values,
                xTickFormatOverride: tick.format,
                phaseToken: `paperlist:${args.view}:${compareActive ? `${args.comparison.conf}${args.comparison.year}` : 'none'}:${args.xaxis}:${args.numBars}:${parsed.summaryOnly ? 'summary' : 'tiered'}`,
            });
        }

        function setView(view) {
            args.view = view;
            renderChart();
        }

        function compareTargetKey() {
            const conf = String(args.comparison.conf || '').toLowerCase();
            const year = String(args.comparison.year || '');
            const track = currentDataset.track || 'main';
            return conf && year ? `${conf}|${year}|${track}` : '';
        }

        function refreshCompareYears() {
            const cfg = window.pc_cmp_cfg || {};
            const idx = cfg.index || {};
            const venueEl = document.getElementById('pc_cmp_venue');
            const yearEl = document.getElementById('pc_cmp_year');
            if (!venueEl || !yearEl) return;
            while (yearEl.options.length > 1) yearEl.remove(1);
            const venue = venueEl.value;
            const self = cfg.self || {};
            const selfTrack = self.track || currentDataset.track || 'main';
            const selfYear = Number(self.year || currentDataset.year || 0);
            if (!venue || !idx[venue]) {
                yearEl.disabled = true;
                args.comparison.year = '';
                return;
            }
            const rows = idx[venue]
                .filter(row => (row.track || 'main') === selfTrack)
                .sort((a, b) => Number(b.year) - Number(a.year));
            rows.forEach(row => {
                if (venue === (self.conf || currentDataset.conf) && Number(row.year) === selfYear) return;
                const opt = document.createElement('option');
                opt.value = row.year;
                opt.textContent = row.year;
                yearEl.appendChild(opt);
            });
            yearEl.disabled = yearEl.options.length <= 1;
            if (args.comparison.year && [...yearEl.options].some(opt => opt.value === String(args.comparison.year))) {
                yearEl.value = args.comparison.year;
            } else {
                yearEl.value = yearEl.options.length > 1 ? yearEl.options[1].value : '';
                args.comparison.year = yearEl.value;
            }
        }

        function populateCompareControls() {
            const cfg = window.pc_cmp_cfg || {};
            const idx = cfg.index || {};
            const venueEl = document.getElementById('pc_cmp_venue');
            if (!venueEl) return;
            Object.keys(idx).sort().forEach(venue => {
                const opt = document.createElement('option');
                opt.value = venue;
                opt.textContent = venue.toUpperCase();
                venueEl.appendChild(opt);
            });
            const defaultVenue = cfg.self && cfg.self.conf && idx[cfg.self.conf]
                ? cfg.self.conf
                : Object.keys(idx).sort()[0] || '';
            args.comparison.conf = defaultVenue;
            venueEl.value = defaultVenue;
            refreshCompareYears();
        }

        function clearCompareDataset() {
            compareDataset = null;
            compareError = '';
        }

        function ensureCompareDataset(onReady) {
            const key = compareTargetKey();
            if (!key) return null;
            if (compareDataset && compareDataset.__key === key) return compareDataset;
            if (compareCache.has(key)) {
                compareDataset = compareCache.get(key);
                return compareDataset;
            }
            if (compareFlights.has(key)) return null;
            const cfg = window.pc_cmp_cfg || {};
            const url = (cfg.ajax_url || (ajaxInfo.ajax_url || '/wp-admin/admin-ajax.php'))
                + '?action=pc_paperlist_cmp_meta'
                + '&conf=' + encodeURIComponent(args.comparison.conf)
                + '&year=' + encodeURIComponent(args.comparison.year)
                + '&track=' + encodeURIComponent(currentDataset.track || 'main');
            const flight = fetch(url, { credentials: 'same-origin' })
                .then(response => response.json())
                .then(js => {
                    if (!js || !js.success || !js.data) {
                        throw new Error((js && js.data && js.data.msg) || 'fetch failed');
                    }
                    const dataset = makeDataset(js.data, {
                        conf: js.data.conf || args.comparison.conf,
                        year: js.data.year || args.comparison.year,
                        track: js.data.track || currentDataset.track || 'main',
                        label: js.data.label,
                    });
                    dataset.__key = key;
                    compareCache.set(key, dataset);
                    compareDataset = dataset;
                    compareError = '';
                    if (typeof onReady === 'function') onReady();
                })
                .catch(error => {
                    compareError = error.message || String(error);
                    compareDataset = null;
                    console.error('[Paperlist comparison] fetch failed:', error);
                })
                .finally(() => {
                    compareFlights.delete(key);
                });
            compareFlights.set(key, flight);
            return null;
        }

        function onclickPaperlistSetting() {
            const guiEl = document.getElementById('gui');
            if (!guiEl) return;
            const next = guiEl.style.display === 'none' || guiEl.style.display === '' ? 'flex' : 'none';
            guiEl.style.display = next;
            const btn = document.getElementById('pc_btn_settings');
            if (btn) btn.classList.toggle('active', next !== 'none');
        }

        function resetChart() {
            const xaxis = args.xaxis;
            Object.assign(args, {
                ...argsInit,
                xaxis,
                comparison: { ...argsInit.comparison },
                line: { ...argsInit.line },
            });
            clearCompareDataset();
            const venueEl = document.getElementById('pc_cmp_venue');
            if (venueEl && venueEl.value) {
                args.comparison.conf = venueEl.value;
                refreshCompareYears();
            }
            renderChart();
        }

        async function downloadChart() {
            const svgElement = document.querySelector('#main-render svg');
            if (!svgElement) return;
            const svgString = new XMLSerializer().serializeToString(svgElement);
            const image = new Image();
            const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            await new Promise(resolve => {
                image.onload = resolve;
                image.src = url;
            });
            const canvas = document.createElement('canvas');
            canvas.width = image.width || args.width;
            canvas.height = image.height || args.height;
            canvas.getContext('2d').drawImage(image, 0, 0);
            URL.revokeObjectURL(url);
            const format = args.downloadFormat;
            const link = document.createElement('a');
            link.download = `${ajaxInfo.conf || 'paperlist'}${ajaxInfo.year || ''}_${ajaxInfo.track || 'main'}_${args.view}_${args.chart}_${args.xaxis}.${format}`;
            link.href = canvas.toDataURL(`image/${format}`);
            link.click();
        }

        function wireControls() {
            $('.pc_phase_pill').on('click', function (event) {
                event.stopPropagation();
                args.comparison.active = false;
                setView(this.dataset.val || args.view);
            });
            $('.pc_view_wrap[data-view="Phase"]').on('click keydown', function (event) {
                if (event.type === 'keydown' && event.key !== 'Enter' && event.key !== ' ') return;
                args.comparison.active = false;
                renderChart();
            });
            $('.pc_view_wrap[data-view="Comparison"]').on('click keydown', function (event) {
                if (event.target.closest('.pc_cmp_select, .pc_cmp_row')) return;
                if (event.type === 'keydown' && event.key !== 'Enter' && event.key !== ' ') return;
                args.comparison.active = !args.comparison.active;
                if (args.comparison.active && !compareTargetKey()) refreshCompareYears();
                renderChart();
            });
            $('#pc_cmp_venue').on('click', event => event.stopPropagation()).on('change', function () {
                args.comparison.conf = this.value;
                clearCompareDataset();
                refreshCompareYears();
                args.comparison.active = true;
                renderChart();
            });
            $('#pc_cmp_year').on('click', event => event.stopPropagation()).on('change', function () {
                args.comparison.year = this.value;
                clearCompareDataset();
                args.comparison.active = true;
                renderChart();
            });
            $('#pc_cmp_mode').on('click', event => event.stopPropagation()).on('change', function () {
                args.comparison.mode = this.value;
                args.comparison.active = true;
                renderChart();
            });
            $('#pc_cmp_merge').on('click', event => event.stopPropagation()).on('change', function () {
                args.comparison.layout = this.value;
                args.comparison.active = true;
                renderChart();
            });
            $('#pc_chart_select').on('change', function () {
                args.chart = this.value;
                if (args.chart === 'Line') args.line.show = true;
                renderChart();
            });
            $('#pc_pl_tile_chart').on('change', function () {
                args.tileChart = this.value;
                renderChart();
            });
            $('#pc_pl_axis').on('change', function () {
                args.xaxis = this.value;
                args.numBars = Math.min(args.numBars, topLimit());
                renderChart();
            });
            $('#pc_pl_top_range, #pc_pl_top_number').on('input change', function () {
                args.numBars = Math.max(1, Math.min(topLimit(), Number(this.value) || args.numBars));
                renderChart();
            });
            $('#pc_pl_width, #pc_pl_height').on('input change', function () {
                args.width = Math.max(400, Math.min(3000, Number($('#pc_pl_width').val()) || args.width));
                args.height = Math.max(260, Math.min(1600, Number($('#pc_pl_height').val()) || args.height));
                renderChart();
            });
            $('#pc_pl_labels').on('change', function () {
                args.showLabels = this.checked;
                renderChart();
            });
            $('#pc_pl_animate').on('change', function () {
                args.animate = this.checked;
                renderChart();
            });
            $('#pc_btn_settings').on('click', onclickPaperlistSetting);
            $(document).on('keydown.pcPaperlistShared', function (event) {
                if (event.which === 'S'.charCodeAt(0)) {
                    onclickPaperlistSetting();
                } else if (event.which === 'R'.charCodeAt(0)) {
                    resetChart();
                }
            });
        }

        buildShell();
        populateCompareControls();
        window.onclick_btn_setting = onclickPaperlistSetting;
        wireControls();
        renderChart();
        window.pc_paperlist = { args, update: renderChart, parseEntries, buildChartData };
    })();
        return true;
    }

    function pcFetchInitialPaperlistMeta() {
        const ajaxInfo = window.ajaxmeta || {};
        const metaObj = window.meta || {};
        if (!metaObj.lazy || !ajaxInfo.ajax_url || !ajaxInfo.conf || !ajaxInfo.year) return;
        const host = document.getElementById('main-render');
        if (host) host.classList.add('pc-chart-loading');
        const url = ajaxInfo.ajax_url
            + '?action=pc_paperlist_cmp_meta'
            + '&conf=' + encodeURIComponent(ajaxInfo.conf)
            + '&year=' + encodeURIComponent(ajaxInfo.year)
            + '&track=' + encodeURIComponent(ajaxInfo.track || 'main');
        fetch(url, { credentials: 'same-origin' })
            .then(response => response.json())
            .then(js => {
                if (!js || !js.success || !js.data) throw new Error((js && js.data && js.data.msg) || 'fetch failed');
                window.meta = js.data;
                pcBootSharedPaperlistChart();
            })
            .catch(error => {
                if (host) host.textContent = 'Chart data fetch failed: ' + (error.message || String(error));
                console.error('[Paperlist] initial meta fetch failed:', error);
            });
    }

    if (!pcBootSharedPaperlistChart()) {
        pcFetchInitialPaperlistMeta();
        return;
    }
    return;

    const AXIS_LABELS = {
        authors: 'Authors',
        authors_id: 'Authors (ID)',
        authors_first: 'First Authors',
        authors_id_first: 'First Authors (ID)',
        authors_last: 'Last Authors',
        authors_id_last: 'Last Authors (ID)',
        affiliations: 'Affiliations / Author',
        affiliations_unique: 'Affiliations / Paper',
        affiliations_first: 'First Author Affiliation',
        affiliations_last: 'Last Author Affiliation',
        affiliations_country: 'Countries / Author',
        affiliations_country_unique: 'Countries / Paper',
        affiliations_country_first: 'First Author Country',
        affiliations_country_last: 'Last Author Country',
        positions: 'Author Positions',
        positions_unique: 'Paper Positions',
        positions_first: 'First Author Position',
        positions_last: 'Last Author Position',
        keywords: 'Keywords',
        keywords_first: 'First Keyword',
    };
    const AXIS_ORDER = Object.keys(AXIS_LABELS);
    const REJECT_RE = /reject|withdraw/i;
    const SINGLE_KEY = 'Count';
    const chartState = {
        svg: null,
        x: d3.scaleBand().padding(0.12),
        y: d3.scaleLinear(),
        hiddenKeys: new Set(),
        lastKeys: [],
    };
    const argsInit = {
        active: 'Accepted',
        xaxis: '',
        numBars: 100,
        showLabels: false,
        showCounts: false,
        animate: true,
        width: 1400,
        height: window.innerWidth / window.innerHeight > 1 ? 560 : 760,
        downloadFormat: 'png',
    };
    const args = { ...argsInit };

    function axisLabel(key) {
        return AXIS_LABELS[key] || key.replace(/_/g, ' ');
    }

    function metricString(axis) {
        const arr = meta.xaxis[axis];
        return Array.isArray(arr) ? String(arr[0] || '') : String(arr || '');
    }

    function parseEntries(text, requestedKeys) {
        const bins = [];
        let summaryOnly = false;
        String(text || '').split(';').forEach((raw, i) => {
            const entry = raw.trim();
            if (!entry) return;
            const parts = entry.split(':');
            if (parts.length < 2) return;
            let label;
            let totalText;
            let countsText = '';
            if (parts.length === 2) {
                label = parts[0];
                totalText = parts[1];
                summaryOnly = true;
            } else {
                countsText = parts.pop();
                totalText = parts.pop();
                label = parts.join(':');
            }
            label = String(label || '').trim();
            const total = Number.parseInt(totalText, 10) || 0;
            if (!label || total <= 0) return;

            const bin = { key: `${i}:${label}`, label, total, rank: i };
            if (summaryOnly || !countsText) {
                bin[SINGLE_KEY] = total;
            } else {
                const counts = countsText.split(',').map(v => Number.parseInt(v, 10) || 0);
                requestedKeys.forEach(status => {
                    const idx = meta.status.indexOf(status);
                    bin[status] = idx >= 0 ? (counts[idx] || 0) : 0;
                });
            }
            bins.push(bin);
        });
        return { bins, summaryOnly };
    }

    function axisHasData(axis) {
        const allStatuses = meta.status.slice();
        return parseEntries(metricString(axis), allStatuses).bins.length > 0;
    }

    const availableAxes = AXIS_ORDER
        .filter(axis => Object.prototype.hasOwnProperty.call(meta.xaxis, axis))
        .concat(Object.keys(meta.xaxis).filter(axis => !AXIS_ORDER.includes(axis)))
        .filter(axisHasData);

    if (!availableAxes.length) return;
    args.xaxis = availableAxes[0];

    function statusKeys() {
        if (args.active === 'Submitted') return meta.status.slice();
        if (args.active === 'Rejected') return meta.status.filter(s => REJECT_RE.test(s));
        return meta.status.filter(s => !REJECT_RE.test(s));
    }

    function colorFor(key) {
        const overrides = {
            Count: '#4062BB',
            Accept: '#4062BB',
            Poster: '#4062BB',
            Spotlight: '#59C3C3',
            Oral: '#F9C74F',
            Conditional: '#89CE94',
            Reject: '#F45B69',
            Withdraw: '#6C757D',
            'Desk Reject': '#343A40',
            'Post Decision Withdraw': '#ADB5BD',
        };
        if (overrides[key]) return overrides[key];
        const idx = Math.max(0, meta.status.indexOf(key));
        return d3.schemeTableau10[idx % d3.schemeTableau10.length];
    }

    function valueFor(d, keys) {
        return keys.reduce((sum, key) => sum + (Number(d[key]) || 0), 0);
    }

    function chartData() {
        let keys = statusKeys();
        let parsed = parseEntries(metricString(args.xaxis), keys);
        if (parsed.summaryOnly || !keys.length) {
            keys = [SINGLE_KEY];
            parsed = parseEntries(metricString(args.xaxis), keys);
        }
        let legendKeys = keys.filter(key => parsed.bins.some(d => (Number(d[key]) || 0) > 0));
        if (!legendKeys.length) legendKeys = [SINGLE_KEY];
        keys = legendKeys;
        if (legendKeys.length > 1) {
            const visible = keys.filter(key => !chartState.hiddenKeys.has(key));
            if (visible.length) keys = visible;
        }
        const data = parsed.bins
            .map(d => ({ ...d, _sum: valueFor(d, keys) }))
            .filter(d => d._sum > 0)
            .sort((a, b) => d3.descending(a._sum, b._sum) || d3.ascending(a.label, b.label))
            .slice(0, args.numBars);
        return { data, keys, legendKeys };
    }

    function injectStyle() {
        if (document.getElementById('pc-paperlist-style')) return;
        const css = `
            .pc-paperlist-visual { margin:8px 0 20px; }
            .pc-pl-toolbar { display:flex; flex-wrap:wrap; align-items:center; gap:10px; padding:12px;
                background:#f3f5f9; border:1px solid #d9dee8; border-radius:8px; margin-bottom:10px; }
            .pc-pl-toolbar label { display:flex; align-items:center; gap:6px; margin:0; font-size:12px; font-weight:600; color:#242833; }
            .pc-pl-toolbar select, .pc-pl-toolbar input[type="number"] { min-height:32px; height:32px; border:1px solid #b8bec7;
                border-radius:6px; background:#fff; color:#242833; font-size:12px; padding:0 8px; }
            .pc-pl-toolbar input[type="range"] { width:130px; accent-color:#4062BB; }
            .pc-pl-toolbar input[type="checkbox"] { accent-color:#4062BB; }
            .pc-pl-status { display:flex; border:1px solid #b8bec7; border-radius:7px; overflow:hidden; background:#fff; }
            .pc-pl-status button, .pc-pl-action { min-height:32px; border:0; border-right:1px solid #d9dee8;
                background:#fff; color:#242833; padding:0 12px; font-size:12px; font-weight:700; cursor:pointer; }
            .pc-pl-status button:last-child { border-right:0; }
            .pc-pl-status button.active, .pc-pl-action.active { background:#4062BB; color:#fff; }
            .pc-pl-action { border:1px solid #b8bec7; border-radius:6px; display:inline-flex; align-items:center; gap:6px; }
            .pc-pl-action .pc_action_gear { transform-origin:50% 50%; transition:transform 600ms ease; }
            .pc-pl-action:hover .pc_action_gear,
            .pc-pl-action.pc-gear-hover .pc_action_gear { transform:rotate(120deg); }
            .pc-pl-toolbar .pc_display_cap_field { flex:1 1 260px; min-width:240px; }
            .pc-pl-toolbar #pc_pl_settings { flex:0 0 auto; white-space:nowrap; }
            .pc-pl-chart { width:100%; overflow:hidden; border:1px solid #e2e6ef; border-radius:8px; background:#fff; }
            .pc-pl-chart svg { display:block; width:100%; height:auto; }
            .pc-pl-empty-state { min-height:220px; display:flex; align-items:center; justify-content:center; color:#687080; font-size:13px; }
            .pc-pl-advanced { display:none; width:100%; gap:10px; flex-wrap:wrap; padding-top:4px; }
            .pc-pl-advanced.open { display:flex; }
            #paperlist { border-collapse:separate; border-spacing:0; width:100%; }
            #paperlist thead th { position:sticky; top:0; z-index:2; background:#f7f8fb; border-bottom:1px solid #d9dee8; }
            #paperlist input { min-height:28px; border:1px solid #c8ced8; border-radius:5px; padding:2px 6px; font-size:12px; }
            #paperlist .sort-btn, #btn_fetchall, #btn_hide_reject { border-radius:5px; font-size:12px; text-decoration:none; cursor:pointer; }
        `;
        document.head.appendChild(Object.assign(document.createElement('style'), { id: 'pc-paperlist-style', textContent: css }));
    }

    function buildShell() {
        injectStyle();
        const axisOptions = availableAxes.map(axis => `<option value="${axis}">${axisLabel(axis)}</option>`).join('');
        const shell = `
            <section class="pc-paperlist-visual">
                <div class="pc-pl-toolbar" id="pc_pl_toolbar">
                    <div class="pc-pl-status" role="group">
                        <button type="button" data-status="Submitted">All Tiers</button>
                        <button type="button" data-status="Accepted">Accepted</button>
                        <button type="button" data-status="Rejected">Rejected</button>
                    </div>
                    <label>Metric <select id="pc_pl_axis">${axisOptions}</select></label>
                    <label class="pc_display_cap_field">Display Cap <input id="pc_pl_top_range" type="range" min="10" max="200" step="1"><input id="pc_pl_top_number" type="number" min="1" max="200" step="1"></label>
                    <label><input id="pc_pl_labels" type="checkbox"> Labels</label>
                    <label><input id="pc_pl_counts" type="checkbox"> Count Overlay</label>
                    <button type="button" class="pc-pl-action" id="pc_pl_settings" title="Advanced settings">${PC_PAPERLIST_GEAR_SVG}<span>Settings [S]</span></button>
                    <div class="pc-pl-advanced" id="pc_pl_advanced">
                        <label>Width <input id="pc_pl_width" type="number" min="400" max="3000" step="50"></label>
                        <label>Height <input id="pc_pl_height" type="number" min="260" max="1600" step="20"></label>
                        <label><input id="pc_pl_animate" type="checkbox"> Animate</label>
                    </div>
                </div>
                <div id="main-render" class="pc-pl-chart"></div>
            </section>`;
        $('#main').prepend(shell);
    }

    function syncControls() {
        $('#pc_pl_axis').val(args.xaxis);
        $('#pc_pl_top_range').val(args.numBars);
        $('#pc_pl_top_number').val(args.numBars);
        $('#pc_pl_labels').prop('checked', args.showLabels);
        $('#pc_pl_counts').prop('checked', args.showCounts);
        $('#pc_pl_animate').prop('checked', args.animate);
        $('#pc_pl_width').val(args.width);
        $('#pc_pl_height').val(args.height);
        $('.pc-pl-status button').toggleClass('active', false)
            .filter(`[data-status="${args.active}"]`).toggleClass('active', true);
    }

    function ensureSvg() {
        if (chartState.svg) return chartState.svg;
        const svg = d3.select('#main-render')
            .append('svg')
            .attr('class', 'pc-paperlist-chart')
            .attr('role', 'img');
        svg.append('g').attr('class', 'pc-pl-grid');
        svg.append('g').attr('class', 'pc-pl-bars');
        svg.append('g').attr('class', 'pc-pl-counts');
        svg.append('g').attr('class', 'pc-pl-x-axis');
        svg.append('g').attr('class', 'pc-pl-y-axis');
        svg.append('g').attr('class', 'pc-pl-axis-labels');
        svg.append('g').attr('class', 'pc-pl-legend');
        svg.append('text').attr('class', 'pc-pl-empty-state').attr('text-anchor', 'middle');
        chartState.svg = svg;
        return svg;
    }

    function updateLegend(svg, keys, margin) {
        const legend = svg.select('.pc-pl-legend')
            .attr('transform', `translate(${args.width - margin.right + 18},${margin.top - 18})`);
        const items = legend.selectAll('g.pc-pl-legend-item').data(keys, d => d);
        items.exit().remove();
        const enter = items.enter()
            .append('g')
            .attr('class', 'pc-pl-legend-item')
            .style('cursor', keys.length > 1 ? 'pointer' : 'default')
            .on('click', (event, key) => {
                if (keys.length <= 1) return;
                if (event.ctrlKey || event.metaKey) {
                    const onlyThisVisible = chartState.lastKeys.length - chartState.hiddenKeys.size === 1 && !chartState.hiddenKeys.has(key);
                    chartState.hiddenKeys = onlyThisVisible
                        ? new Set()
                        : new Set(chartState.lastKeys.filter(k => k !== key));
                } else if (chartState.hiddenKeys.has(key)) {
                    chartState.hiddenKeys.delete(key);
                } else {
                    chartState.hiddenKeys.add(key);
                }
                updateChart();
            });
        enter.append('rect').attr('width', 12).attr('height', 12).attr('rx', 2);
        enter.append('text').attr('x', -7).attr('y', 10).attr('text-anchor', 'end').attr('font-size', 11);
        enter.merge(items)
            .attr('transform', (d, i) => `translate(0,${i * 18})`)
            .attr('opacity', d => chartState.hiddenKeys.has(d) ? 0.32 : 1);
        enter.merge(items).select('rect').attr('fill', d => colorFor(d));
        enter.merge(items).select('text').text(d => d).attr('fill', '#242833');
    }

    function updateChart() {
        syncControls();
        const { data, keys, legendKeys } = chartData();
        chartState.lastKeys = legendKeys;
        const svg = ensureSvg();
        const width = args.width;
        const height = args.height;
        const margin = { top: 46, right: Math.max(150, Math.min(240, keys.length * 28)), bottom: args.showLabels ? 170 : 76, left: 70 };
        const innerRight = width - margin.right;
        const duration = args.animate ? 520 : 0;
        const t = svg.transition().duration(duration).ease(d3.easeCubicOut);

        svg.attr('viewBox', [0, 0, width, height]).attr('width', width).attr('height', height);
        svg.select('.pc-pl-empty-state')
            .attr('x', width / 2)
            .attr('y', height / 2)
            .attr('font-size', 14)
            .attr('fill', '#687080')
            .text(data.length ? '' : 'No chart data available');
        if (!data.length) {
            svg.selectAll('.pc-pl-grid line,.pc-pl-bars g,.pc-pl-counts text,.pc-pl-x-axis *,.pc-pl-y-axis *,.pc-pl-axis-labels *,.pc-pl-legend *').remove();
            return;
        }

        chartState.x.domain(data.map(d => d.key)).range([margin.left, innerRight]);
        const maxY = d3.max(data, d => d._sum) || 1;
        chartState.y.domain([0, maxY]).nice().range([height - margin.bottom, margin.top]);
        const stack = d3.stack().keys(keys)(data);

        const yTicks = chartState.y.ticks(7);
        const grid = svg.select('.pc-pl-grid').selectAll('line').data(yTicks, d => d);
        grid.exit().transition(t).attr('opacity', 0).remove();
        grid.enter().append('line')
            .attr('x1', margin.left)
            .attr('x2', innerRight)
            .attr('y1', chartState.y(0))
            .attr('y2', chartState.y(0))
            .attr('stroke', '#d9dee8')
            .attr('stroke-width', 1)
            .attr('stroke-dasharray', '4 5')
            .attr('opacity', 0)
            .merge(grid)
            .transition(t)
            .attr('x1', margin.left)
            .attr('x2', innerRight)
            .attr('y1', d => chartState.y(d))
            .attr('y2', d => chartState.y(d))
            .attr('opacity', d => d === 0 ? 0 : 0.75);

        const series = svg.select('.pc-pl-bars').selectAll('g.pc-pl-series').data(stack, d => d.key);
        series.exit().remove();
        const seriesEnter = series.enter().append('g').attr('class', 'pc-pl-series');
        const seriesMerge = seriesEnter.merge(series).attr('fill', d => colorFor(d.key));
        stack.forEach(layer => layer.forEach(d => { d.key = layer.key; }));

        const rects = seriesMerge.selectAll('rect').data(d => d, d => `${d.data.key}:${d.key}`);
        rects.exit().transition(t)
            .attr('y', chartState.y(0))
            .attr('height', 0)
            .remove();
        const rectEnter = rects.enter().append('rect')
            .attr('x', d => chartState.x(d.data.key))
            .attr('width', chartState.x.bandwidth())
            .attr('y', chartState.y(0))
            .attr('height', 0)
            .attr('rx', 2)
            .attr('shape-rendering', 'geometricPrecision');
        rectEnter.append('title');
        rectEnter.merge(rects)
            .transition(t)
            .attr('x', d => chartState.x(d.data.key))
            .attr('width', chartState.x.bandwidth())
            .attr('y', d => chartState.y(d[1]))
            .attr('height', d => Math.max(0, chartState.y(d[0]) - chartState.y(d[1])));
        seriesMerge.selectAll('rect title')
            .text(d => `${d.data.label}\n${d.key}: ${d[1] - d[0]}\nTotal: ${d.data._sum}`);

        const labelEvery = chartState.x.bandwidth() < 18 ? Math.ceil(18 / Math.max(1, chartState.x.bandwidth())) : 1;
        const countData = args.showCounts
            ? data.filter((d, i) => i % labelEvery === 0)
            : [];
        const labels = svg.select('.pc-pl-counts').selectAll('text').data(countData, d => d.key);
        labels.exit().transition(t).attr('opacity', 0).remove();
        labels.enter().append('text')
            .attr('text-anchor', 'middle')
            .attr('font-size', 10)
            .attr('fill', '#242833')
            .attr('opacity', 0)
            .merge(labels)
            .transition(t)
            .attr('x', d => chartState.x(d.key) + chartState.x.bandwidth() / 2)
            .attr('y', d => chartState.y(d._sum) - 6)
            .attr('opacity', 1)
            .text(d => d._sum);

        const tickStep = args.showLabels ? Math.max(1, Math.ceil(data.length / 34)) : Math.max(1, Math.ceil(data.length / 28));
        const tickValues = data.map(d => d.key).filter((d, i) => i % tickStep === 0);
        const xAxis = d3.axisBottom(chartState.x)
            .tickValues(tickValues)
            .tickSizeOuter(0)
            .tickFormat(key => {
                const idx = data.findIndex(d => d.key === key);
                return args.showLabels ? data[idx]?.label || '' : String(idx + 1);
            });
        svg.select('.pc-pl-x-axis')
            .attr('transform', `translate(0,${height - margin.bottom})`)
            .transition(t)
            .call(xAxis)
            .selection()
            .selectAll('text')
            .attr('fill', '#242833')
            .attr('font-size', 10)
            .attr('dx', args.showLabels ? 6 : 0)
            .attr('dy', args.showLabels ? -5 : 12)
            .attr('transform', args.showLabels ? 'rotate(-68)' : null)
            .style('text-anchor', args.showLabels ? 'start' : 'middle');

        svg.select('.pc-pl-y-axis')
            .attr('transform', `translate(${margin.left},0)`)
            .transition(t)
            .call(d3.axisLeft(chartState.y).ticks(7).tickSizeOuter(0))
            .selection()
            .call(g => g.select('.domain').remove())
            .selectAll('text')
            .attr('fill', '#242833')
            .attr('font-size', 11);

        const axisLabels = svg.select('.pc-pl-axis-labels');
        axisLabels.selectAll('text').data([
            { key: 'title', x: margin.left, y: 24, anchor: 'start', text: `${axisLabel(args.xaxis)} by ${args.active} count` },
            { key: 'y', x: 0, y: margin.top - 26, anchor: 'start', text: 'Count' },
            { key: 'x', x: innerRight, y: height - 28, anchor: 'end', text: args.showLabels ? axisLabel(args.xaxis) : `${axisLabel(args.xaxis)} rank` },
        ], d => d.key)
            .join('text')
            .attr('x', d => d.x)
            .attr('y', d => d.y)
            .attr('fill', '#242833')
            .attr('font-size', d => d.key === 'title' ? 14 : 12)
            .attr('font-weight', d => d.key === 'title' ? 700 : 600)
            .attr('text-anchor', d => d.anchor)
            .text(d => d.text);

        updateLegend(svg, legendKeys, margin);
    }

    function toggleSettings() {
        $('#pc_pl_advanced').toggleClass('open');
        $('#pc_pl_settings').toggleClass('active', $('#pc_pl_advanced').hasClass('open'));
    }

    function resetChart() {
        const active = args.active;
        const xaxis = args.xaxis;
        Object.assign(args, argsInit, { active, xaxis });
        chartState.hiddenKeys.clear();
        updateChart();
    }

    async function downloadChart() {
        const svgElement = document.querySelector('#main-render svg');
        if (!svgElement) return;
        const svgString = new XMLSerializer().serializeToString(svgElement);
        const canvas = document.createElement('canvas');
        const image = new Image();
        const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        await new Promise(resolve => {
            image.onload = resolve;
            image.src = url;
        });
        canvas.width = image.width;
        canvas.height = image.height;
        canvas.getContext('2d').drawImage(image, 0, 0);
        URL.revokeObjectURL(url);
        const link = document.createElement('a');
        link.download = `${ajaxmeta.conf}${ajaxmeta.year}_${ajaxmeta.track}_${args.active}_${args.xaxis}.${args.downloadFormat}`;
        link.href = canvas.toDataURL(`image/${args.downloadFormat}`);
        link.click();
    }

    buildShell();
    syncControls();

    $('.pc-pl-status button').on('click', function () {
        args.active = $(this).data('status');
        chartState.hiddenKeys.clear();
        updateChart();
    });
    $('#pc_pl_axis').on('change', function () {
        args.xaxis = this.value;
        chartState.hiddenKeys.clear();
        updateChart();
    });
    $('#pc_pl_top_range, #pc_pl_top_number').on('input change', function () {
        args.numBars = Math.max(1, Math.min(200, Number(this.value) || args.numBars));
        updateChart();
    });
    $('#pc_pl_labels').on('change', function () {
        args.showLabels = this.checked;
        updateChart();
    });
    $('#pc_pl_counts').on('change', function () {
        args.showCounts = this.checked;
        updateChart();
    });
    $('#pc_pl_animate').on('change', function () {
        args.animate = this.checked;
        updateChart();
    });
    $('#pc_pl_width, #pc_pl_height').on('input change', function () {
        args.width = Math.max(400, Math.min(3000, Number($('#pc_pl_width').val()) || args.width));
        args.height = Math.max(260, Math.min(1600, Number($('#pc_pl_height').val()) || args.height));
        updateChart();
    });
    $('#pc_pl_settings').on('click', toggleSettings);

    $(document).keydown(function (e) {
        if (pcPaperlistIsTextEntryHotkeyTarget(e)) return;
        if (e.which === 'S'.charCodeAt(0)) {
            toggleSettings();
        } else if (e.ctrlKey && e.which === 'R'.charCodeAt(0)) {
            resetChart();
        }
    });

    updateChart();
});
