// script.js
// Dynamically populates dropdowns by calling /api/distinct-values
// Renders a D3 bar chart from either /api/data or /api/filter

document.addEventListener("DOMContentLoaded", () => {
  populateDropdowns();
  const btnFilter = document.getElementById("btnFilter");
  btnFilter.addEventListener("click", applyFilter);

  // Initial: fetch all data and display
  fetchDataAndRender("/api/data");
});

function populateDropdowns() {
  d3.json("/api/distinct-values")
    .then((data) => {
      const sectors = data.sectors || [];
      const regions = data.regions || [];

      const sectorSelect = document.getElementById("sectorSelect");
      const regionSelect = document.getElementById("regionSelect");

      // Clear existing options & add "All"
      sectorSelect.innerHTML = "";
      regionSelect.innerHTML = "";

      sectorSelect.appendChild(createOption("", "All"));
      regionSelect.appendChild(createOption("", "All"));

      sectors.forEach((sec) => {
        sectorSelect.appendChild(createOption(sec, sec));
      });
      regions.forEach((reg) => {
        regionSelect.appendChild(createOption(reg, reg));
      });
    })
    .catch((error) => console.error("Error fetching distinct values:", error));
}

function createOption(value, text) {
  const opt = document.createElement("option");
  opt.value = value;
  opt.textContent = text;
  return opt;
}

function applyFilter() {
  const sector = document.getElementById("sectorSelect").value;
  const region = document.getElementById("regionSelect").value;
  const year = document.getElementById("yearSelect").value.trim();

  let queries = [];
  if (sector) queries.push(`sector=${sector}`);
  if (region) queries.push(`region=${region}`);
  if (year) queries.push(`year=${year}`);

  const queryString = queries.length ? `?${queries.join("&")}` : "";
  const url = `/api/filter${queryString}`;

  fetchDataAndRender(url);
}

function fetchDataAndRender(url) {
  d3.json(url)
    .then((data) => {
      // Clear any previous chart
      d3.select("#chartArea").selectAll("*").remove();

      // Example: group data by country, sum intensities
      const grouped = d3.rollup(
        data,
        (v) => d3.sum(v, (d) => d.intensity || 0),
        (d) => d.country || "Unknown"
      );
      const chartData = Array.from(grouped, ([country, intensity]) => ({ country, intensity }));

      // Chart dimensions
      const margin = { top: 20, right: 20, bottom: 60, left: 50 };
      const width = 600;
      const height = 400;

      // Create SVG
      const svg = d3
        .select("#chartArea")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      // X scale
      const xScale = d3
        .scaleBand()
        .domain(chartData.map((d) => d.country))
        .range([margin.left, width - margin.right])
        .padding(0.1);

      // Y scale
      const yMax = d3.max(chartData, (d) => d.intensity);
      const yScale = d3
        .scaleLinear()
        .domain([0, yMax || 0])
        .range([height - margin.bottom, margin.top]);

      // X-axis
      svg
        .append("g")
        .attr("transform", `translate(0, ${height - margin.bottom})`)
        .call(d3.axisBottom(xScale))
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");

      // Y-axis
      svg
        .append("g")
        .attr("transform", `translate(${margin.left}, 0)`)
        .call(d3.axisLeft(yScale));

      // Draw bars
      svg
        .selectAll(".bar")
        .data(chartData)
        .join("rect")
        .attr("class", "bar")
        .attr("x", (d) => xScale(d.country))
        .attr("y", (d) => yScale(d.intensity))
        .attr("width", xScale.bandwidth())
        .attr("height", (d) => height - margin.bottom - yScale(d.intensity));
    })
    .catch((error) => console.error("Error fetching data:", error));
}