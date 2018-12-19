function buildSpan(tag) {
  const innerText = tag.innerText
  const correctIdx = tag.index

  const spanElem = document.createElement('span')
  spanElem.classList = 'word'
  spanElem.innerText = innerText
  spanElem.setAttribute('data-idx', correctIdx)
  return spanElem
}

function parseString(start, endIncl) {
  const words = []
  for (let idx = start; idx <= endIncl; ++idx) {
    words.push(tags[idx].word)
  }

  return words.join(' ')
}

let currMode = 'entity'
let selectedIdxs = []
let exprIdxs = []
let entity = null
let entityString = null
let attribute = null
let attributeString = null
let sentiment = null

const entityMode = {
  setup: () => {
    helpText.innerHTML = 'Select ENTITY from DROPDOWN.'
    btnEntity.disabled = false
  },
  btn: btnEntity,
  singleHandler: (tagIdx) => {
    entityString = entityDropdown.value
    entity = tags[entityEntries[entityString]['start']]
  },
  multiHandler: (startIdx, endIdx, primaryIdx) => {
    entityMode[singleHandler](startIdx)
  },
  nextMode: () => {
    btnEntity.children[0].innerHTML = ''
    btnEntity.disabled = true
    selectedIdxs = []
    currMode = 'attribute'
  }
}

const attrMode = {
  setup: () => {
    helpText.innerHTML = `Entity OK. Select ATTRIBUTE for '${entity.word}'`
  },
  btn: btnAttr,
  singleHandler: (tagIdx) => {
    const attrTag = tags[tagIdx]
    attrTag.setAttribute(entity)
    attribute = attrTag
    attributeString = parseString(tagIdx, tagIdx)
  },
  multiHandler: (startIdx, endIdx, primaryIdx) => {
    const attrTag = tags[primaryIdx]
    for (let idx = startIdx; idx <= endIdx; ++idx) {
      if (idx != primaryIdx) tags[idx].setChild(attrTag)
    }
    attrTag.setAttribute(entity)
    attribute = attrTag
    attributeString = parseString(startIdx, endIdx)
  },
  nextMode: () => {
    btnAttr.children[0].innerHTML = ''
    btnAttr.disabled = true
    selectedIdxs = []

    let sentiment = -2
    while (sentiment != null && (sentiment < -1 || sentiment > 1)) {
      sentiment = prompt('(Optional) tag the sentiment score between -1 and 1 inclusive.', 'Leave blank if not applicable.')
      if (sentiment.length == 0) sentiment = null
    }

    updateTaggedData(sentiment)

    // Reset variables
    entity = null
    entityString = null
    attribute = null
    attributeString = null
    selected.innerHTML = 'Selected: '

    currMode = 'entity'
  }
}

function updateTaggedData(sentiment) {

  const [start, end] = exprIdxs
  const expr = parseString(start, end)

  // Tagged elements: no further processing required
  spacyConsole.innerHTML = JSON.stringify(createAnnotations(), null, 2)

  // Sentiment (if applicable)
  if (sentiment != null) {
    sentiment = Number(sentiment)

    const sentimentEntry = { expr: expr, sentiment: sentiment } 
    sentimentEntries.push(sentimentEntry)
    sentimentConsole.innerHTML += `("${expr}", ${sentiment})\n`
  }
  
  // Model output
  const modelEntry = { entity: entityString, attribute: attributeString, expression: expr };
  if (sentiment != null) modelEntry['sentiment'] = sentiment

  modelEntries.push(modelEntry)
  modelConsole.innerHTML += `("${entityString}", "${attributeString}", "${expr}" ${sentiment == null ? "" : (", " + sentiment)})\n`

  tagCount.innerHTML = Number(tagCount.innerHTML) + 1
}

const modes = {
  entity: entityMode, attribute: attrMode
}

function textSelected(event) {
  // Ignore if nothing selected
  const selection = window.getSelection()
  if (!selection) return

  // Ignore if no text selected
  if (selection.rangeCount == 0) return

  // Ignore if text selection is outside window
  const range = selection.getRangeAt(0)
  if (range.startContainer.parentNode.classList != 'word') return

  const startIdx = Number(range.startContainer.parentNode.getAttribute('data-idx'))
  const endIdx = Number(range.endContainer.parentNode.getAttribute('data-idx'))

  const parent = range.startContainer.parentNode.parentNode
  const count = endIdx - startIdx + 1

  if (parent == mainWindow) {
    initAnnotationWindow(startIdx, endIdx)
  } else if (parent == entityWindow) {
  
    btnSelectEntity.disabled = false
    btnSelectEntity.children[0].innerHTML = count

    entityIdxs = (startIdx == endIdx) ? [startIdx] : [startIdx, endIdx]
  } else if (currMode == 'attribute') {

    // Enable the corresponding button and update the badge
    modes[currMode].btn.disabled = false
    modes[currMode].btn.children[0].innerHTML = count

    selectedIdxs = (startIdx == endIdx) ? [startIdx] : [startIdx, endIdx]

    selected.innerHTML = 'Selected: ' + parseString(startIdx, endIdx)
  }
}

function onTagClick(event) {
  if (selectedIdxs.length <= 1) {
    modes[currMode].singleHandler(selectedIdxs[0])
    modes[currMode].nextMode()
    modes[currMode].setup()
  } else {
    // Initialise modal for selection
    initSelectionModal()
    $('#multiSelectModal').modal('show')
  }
}

function initSelectionModal() {
  modalHead.innerHTML = `Multi-Word: ${currMode.toUpperCase()}`
  modalSelect.innerHTML = ''

  const [startIdx, stopIdx] = selectedIdxs
  for (let idx = startIdx; idx <= stopIdx; ++idx) {
    const option = document.createElement('option')
    option.innerHTML = `${idx}: ${tags[idx].word}`
    modalSelect.appendChild(option)
  }
}

function onModalSaveClick(event) {
  const primaryIdx = parseInt(modalSelect.value.split(':')[0]) 
  const [startIdx, stopIdx] = selectedIdxs
  $('#multiSelectModal').modal('hide')
  modes[currMode].multiHandler(startIdx, stopIdx, primaryIdx)
  modes[currMode].nextMode()
  modes[currMode].setup()
}

function initAnnotationWindow(startIdx, endIdxIncl) {
  // Reset annotation window elements
  annotationWindow.innerHTML = ''

  exprIdxs = [startIdx, endIdxIncl]
  for (let idx = startIdx; idx <= endIdxIncl; ++idx) {
    const tag = tags[idx]
    console.log(tag)
    const span = buildSpan(tag)
    annotationWindow.appendChild(span)
  }

  modes[currMode].setup()
}

// Text selection listener
document.onmouseup = textSelected

// Actual tagging buttons
btnEntity.addEventListener('click', onTagClick)
btnAttr.addEventListener('click', onTagClick)
modalSave.addEventListener('click', onModalSaveClick)