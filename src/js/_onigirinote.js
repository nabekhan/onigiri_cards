// 1. Split hierarchical tags
var tagsContainer = document.querySelector(".onigiri-tags");
if (tagsContainer) {
  var tagsContainerEl = document.querySelectorAll(".onigiri-tags > *");
  if (tagsContainerEl.length > 0) {
    tagsContainerEl.forEach((tagEl) => {
      tagEl.classList.add("onigiri-tag");
      var parts = tagEl.innerHTML.split("::").filter(Boolean);
      tagEl.innerHTML = parts[parts.length - 1].trim();
    });
  } else {
    var tags = tagsContainer.innerHTML.split(" ").filter(Boolean);
    var html = "";
    tags.forEach((tag) => {
      var childTag = tag.split("::").filter(Boolean);
      html +=
        "<span class='onigiri-tag'>" +
        childTag[childTag.length - 1].trim() +
        "</span>";
    });
    tagsContainer.innerHTML = html;
  }
}

// 2. Breadcrumbs to current deck
var deckEl = document.querySelector(".onigiri-deck");
if (deckEl) {
  var subDecks = deckEl.innerHTML.split("::").filter(Boolean);
  var html = [];
  subDecks.forEach((subDeck) => {
    html.push("<span class='onigiri-subdeck'>" + subDeck.trim() + "</span>");
  });
  deckEl.innerHTML = html.join("&nbsp;/&nbsp;");
}