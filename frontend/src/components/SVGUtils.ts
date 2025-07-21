export function createSvgFromPaths(paths: {x:number,y:number}[][], width = 600, height = 600):HTMLElement {
  const svg = document.createElement('svg');
  svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  svg.setAttribute("width", width.toString());
  svg.setAttribute("width", width.toString());
  svg.setAttribute("height", height.toString());
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);

  paths.forEach(pathPoints => {
    if (pathPoints.length === 0) return;

    const d = pathPoints.map((point, i) => {
      const x = point.x
      const y = point.y;
      return i === 0 ? `M ${x} ${y}` : `L ${x} ${y}`
    }).join(" ");

    const path = document.createElement("path");
    path.setAttribute("d", d);
    path.setAttribute("stroke", "black");
    path.setAttribute("fill", "none");
    path.setAttribute("stroke-width", "2");

    svg.appendChild(path);
  });
  return svg;
}
