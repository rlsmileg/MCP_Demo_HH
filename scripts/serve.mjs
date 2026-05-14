import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { createServer } from "node:http";
import path from "node:path";

const root = process.cwd();
const rootPath = path.resolve(root);
const port = Number(process.env.PORT || 4173);
const types = new Map([
  [".html", "text/html; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
]);

function safePath(url) {
  const pathname = decodeURIComponent(new URL(url, `http://localhost:${port}`).pathname);
  const requested = pathname === "/" ? "/index.html" : pathname;
  const resolved = path.resolve(rootPath, `.${requested}`);

  if (!resolved.startsWith(rootPath)) {
    return null;
  }

  return resolved;
}

createServer(async (request, response) => {
  const filePath = safePath(request.url || "/");

  if (!filePath) {
    response.writeHead(403);
    response.end("Forbidden");
    return;
  }

  try {
    const info = await stat(filePath);

    if (!info.isFile()) {
      response.writeHead(404);
      response.end("Not found");
      return;
    }

    response.writeHead(200, {
      "content-type": types.get(path.extname(filePath)) || "application/octet-stream",
    });
    createReadStream(filePath).pipe(response);
  } catch {
    response.writeHead(404);
    response.end("Not found");
  }
}).listen(port, () => {
  console.log(`Serving http://localhost:${port}`);
});
