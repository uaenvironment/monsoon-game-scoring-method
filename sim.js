
const svgHeight = 500;
const svgWidth = 500;
const bigMargin = 40;
const smallMargin = 10;
const rectWidth = (svgWidth - bigMargin - smallMargin) / 80;

let xScale = d3.scaleLinear();
let yScale = d3.scaleLinear();
let method = 'a';

function createSvg(sel) {
    return sel
        .append("svg")
        .attr("id", `svg-${method}`)
        .attr("width", svgWidth)
        .attr("height", svgHeight);
}

function setScales() {
    // set scales for each graph
    // scales are set for a guess number of 1000
    xScale
        .domain([0, 90])
        .range([bigMargin, svgWidth - smallMargin]);
    yScale
        .domain([0, 80])
        .range([svgHeight - bigMargin, smallMargin])
}

function createRects(sel) {
    return sel
        .append("g")
        .selectAll("rect")
        .data(data[method])
        .enter()
        .append("rect")
        .attr("x", d => xScale(d.x) + rectWidth)
        .attr("y", d => yScale(d.y))
        .attr("width", rectWidth)
        .attr("height", d => svgHeight - bigMargin - yScale(d.y))
        .attr('fill', '#3AABFF')
        .attr('stroke', 'black')
}

function getAxes() {
    // axes
    d3.select(`#svg-${method}`)
        .append('g')
        .attr('id', 'xaxis')
        .attr('transform', `translate(0, ${svgHeight - bigMargin})`)
        .call(xAxis);
    d3.select(`#svg-${method}`)
        .append('g')
        .attr('id', 'yaxis')
        .attr('transform', `translate(${bigMargin}, 0)`)
        .call(yAxis);
    // labels
    d3.select(`#svg-${method}`)
        .append("text")
        .attr("x", 50)
        .attr("y", 40)
        .text(`Scoring Method ${(method)}`)
    d3.select(`#svg-${method}`)
        .append("text")
        .attr("x", 190)
        .attr("y", 500)
        .text(`Total Points for the Year`)
    d3.select(`#svg-${method}`)
        .append("text")
        .attr("x", 12)
        .attr("y", 300)
        .attr("transform", 'rotate(270, 12, 300)')
        .text(`Number of Occurences`)
}

d3.selection.prototype.callAndReturn = function (callable) {
    return callable(this);
};

const xAxis = d3.axisBottom(xScale);
const yAxis = d3.axisLeft(yScale);

/** create it all */
setScales()

// original scoring functions
d3.select("#plot-a")
    .callAndReturn(createSvg)
    .callAndReturn(createRects);
getAxes()

method = 'b';
d3.select("#plot-b")
    .callAndReturn(createSvg)
    .callAndReturn(createRects);
getAxes()

method = 'c';
d3.select("#plot-c")
    .callAndReturn(createSvg)
    .callAndReturn(createRects);
getAxes()

// skewed scoring functions
method = 'd';
d3.select("#plot-d")
    .callAndReturn(createSvg)
    .callAndReturn(createRects);
getAxes()

method = 'e';
d3.select("#plot-e")
    .callAndReturn(createSvg)
    .callAndReturn(createRects);
getAxes()

method = 'f';
d3.select("#plot-f")
    .callAndReturn(createSvg)
    .callAndReturn(createRects);
getAxes()