// Constants
const DEFAULT_HEAD = 0
const DEFAULT_DEP = '-'

// DOM
const fileUpload = document.getElementById('fileUpload')
const annotationWindow = document.getElementById('annotationWindow')
const textArea = document.getElementById('textArea')
const instructions = document.getElementById('helptext')
const exportName = document.getElementById('exportName')
const exportButton = document.getElementById('exportJSON')
const consoleWindow = document.getElementById('console')

// Objects
class TagElement {

  constructor(word, index) {
    this.word = word
    this.index = index
    this.head = DEFAULT_HEAD
    this.dep = DEFAULT_DEP
  }

  setEntity() {
    this.head = this.index
    this.dep = 'ENTITY'
  }

  setAttribute(entityTag) {
    this.head = entityTag.index
    this.dep = 'ATTRIBUTE'
  }

  setSentiment(attributeTag) {
    this.head = attributeTag.index
    this.dep = 'SENTIMENT'
  }

}

var text = ""
const tags = []

function mockText() {
  text = 'The iPhone has a great camera but bad specs.'
}

function loadText() {
  let text = textArea.value

  // Reset annotation window
  annotationWindow.innerHTML = ''

  // Split on whitespace
  const words = text.split(new RegExp('[ \w\b\n]')).filter(x => x != '')
  words.forEach((word, idx) => {
    const tag = new TagElement(word, idx)

    const spanElement = document.createElement('span')
    spanElement.classList.add('word')
    spanElement.innerText = word + ' '
    spanElement.addEventListener('click', () => handleDependency(idx))

    tags.push(tag)
    annotationWindow.appendChild(spanElement)
  })

  console.log(tags)
}

var entity = null
var attribute = null
const modes = ['entity', 'attribute', 'sentiment']
var modeIdx = 0

function nextMode() {
  modeIdx = (modeIdx + 1) % 3
  updateHelpText()
}

function updateHelpText() {
  let helpText = ''

  switch (modes[modeIdx]) {
    case 'entity':
      helpText = 'select ENTITY'
      break

    case 'attribute':
      helpText = `select ATTRIBUTE for entity '${entity.word}'`
      break

    default:
      helpText = `select SENTIMENT for attribute '${attribute.word}' of entity '${entity.word}' `
  }

  instructions.innerHTML = 'Current mode: ' + helpText
}

function handleDependency(idx) {
  const tag = tags[idx]

  switch (modes[modeIdx]) {
    case 'entity':
      tag.setEntity()
      entity = tag
      break
    case 'attribute':
      tag.setAttribute(entity)
      attribute = tag
      break
    default:
      tag.setSentiment(attribute)
      
      // Reset
      entity = null
      attribute = null

      // Print to consle
      printAnnotations()
  }

  nextMode()
}

function printAnnotations() {
  const annotations = createAnnotations()
  consoleWindow.innerHTML = `<pre>${JSON.stringify(annotations, null, 2)}</pre>`
}

function createAnnotations() {
  const heads = tags.map(tag => tag.head)
  const deps = tags.map(tag => tag.dep)

  return {
    text: text,
    heads: heads,
    deps: deps
  }
}

function exportJSON(event) {
  // Get filename
  let name = exportName.value
  if (name == '') {
    alert('Export name required.')
    return
  }

  const annotations = JSON.stringify(createAnnotations())
  if (!name.endsWith('.json')) name += '.json'

  // Create file
  const element = document.createElement('a')
  element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(annotations))
  element.setAttribute('download', name)
  element.click()
}

function readFile(event) {
  const file = fileUpload.files[0]
  console.log(file)
  if (!file) return

  const fileReader = new FileReader()
  fileReader.onload = event => textArea.value = event.target.result
  fileReader.onerror = _ => textArea.value = 'Error reading file'

  fileReader.readAsText(file, 'utf-8')
}

loadText()
updateHelpText()
exportButton.addEventListener('click', exportJSON)
fileUpload.addEventListener('change', readFile)