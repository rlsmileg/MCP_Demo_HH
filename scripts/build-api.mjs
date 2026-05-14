import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const csvPath = path.join(root, "myDatasauRus.csv");
const apiDir = path.join(root, "api");
const datasetDir = path.join(apiDir, "datasets");

function parseCsv(text) {
  const [headerLine, ...lines] = text.trim().split(/\r?\n/);
  const headers = headerLine.split(",");

  return lines.map((line) => {
    const values = line.split(",");
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

function toPoint(row) {
  return {
    x: Number(row.x),
    y: Number(row.y),
  };
}

function summary(points) {
  const xs = points.map((point) => point.x);
  const ys = points.map((point) => point.y);

  return {
    count: points.length,
    x: {
      min: Math.min(...xs),
      max: Math.max(...xs),
    },
    y: {
      min: Math.min(...ys),
      max: Math.max(...ys),
    },
  };
}

const rows = parseCsv(await readFile(csvPath, "utf8"));
const datasets = new Map();

for (const row of rows) {
  if (!datasets.has(row.dataset)) {
    datasets.set(row.dataset, []);
  }

  datasets.get(row.dataset).push(toPoint(row));
}

await mkdir(datasetDir, { recursive: true });

const index = [...datasets.entries()]
  .sort(([a], [b]) => a.localeCompare(b))
  .map(([name, points]) => ({
    name,
    count: points.length,
    url: `datasets/${encodeURIComponent(name)}.json`,
  }));

await writeFile(
  path.join(apiDir, "datasets.json"),
  `${JSON.stringify({ datasets: index }, null, 2)}\n`,
);

for (const [name, points] of datasets.entries()) {
  await writeFile(
    path.join(datasetDir, `${name}.json`),
    `${JSON.stringify({ dataset: name, points, summary: summary(points) }, null, 2)}\n`,
  );
}

console.log(`Built ${datasets.size} dataset API files.`);
