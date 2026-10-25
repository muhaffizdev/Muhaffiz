import { Graphviz } from "/tmp/claude-1000/-home-shamoil--claude-spares-spare-NaG91a/3b67b8b7-f019-42e4-99a4-0e7e45cc0dec/scratchpad/gv/node_modules/@hpcc-js/wasm-graphviz/dist/index.js";
import fs from "fs";
const gv = await Graphviz.load();
const [,, inp, outp, engine] = process.argv;
const svg = gv.layout(fs.readFileSync(inp, "utf8"), "svg", engine || "dot");
fs.writeFileSync(outp, svg);
