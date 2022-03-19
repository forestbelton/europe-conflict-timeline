// NOTE: Copy/paste into developer console on Wikipedia page and then copy
// document contents (https://en.wikipedia.org/wiki/List_of_conflicts_in_Europe)
const rawEntries = [
  ...document.querySelectorAll(".mw-parser-output > ul > li"),
].map((node) => node.textContent);
document.body.textContent = JSON.stringify(rawEntries);
