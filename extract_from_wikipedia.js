const rawEntries = [
  ...document.querySelectorAll(".mw-parser-output > ul > li"),
].map((node) => node.textContent);
document.body.textContent = JSON.stringify(rawEntries);
