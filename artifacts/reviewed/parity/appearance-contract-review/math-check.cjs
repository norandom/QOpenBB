const fs = require('node:fs');
const { _Util: { Color } } = require('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/ag-charts-community/dist/package/main.cjs.js');
const hex = channel => `#${channel.toString(16).padStart(2, '0')}0000`;
const checks = [];
for (const t of [1 - .257, 1 - .1, .57, .38]) {
  let mismatches = 0;
  const examples = [];
  for (let foreground = 0; foreground < 256; foreground++) {
    for (let background = 0; background < 256; background++) {
      const direct = Math.round(foreground * (1 - t) + background * t);
      const sourceHex = Color.mix(Color.fromString(hex(foreground)), Color.fromString(hex(background)), t).toString();
      const source = Number.parseInt(sourceHex.slice(1, 3), 16);
      const normalized = Math.round(Math.max(0, Math.min(1, (foreground / 255) * (1 - t) + (background / 255) * t)) * 255);
      if (normalized !== source) throw Error('Normalized source mismatch');
      if (direct !== source) {
        mismatches++;
        if (examples.length < 5) examples.push({ foreground, background, direct, source, sourceHex });
      }
    }
  }
  checks.push({ t, pairs: 65536, mismatches, examples });
}
const result = { directByteFormulaEquivalent: checks.every(c => c.mismatches === 0), normalizedFormulaEquivalent: true, checks };
fs.writeFileSync('/mnt/d/Source/QOpenBB/artifacts/parity/appearance-contract-review/math-check.json', JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result));
process.exitCode = result.directByteFormulaEquivalent ? 0 : 1;
