// DOM elements
const fileUpload = document.querySelector('#fileUpload')
const textArea = document.querySelector('#textArea')
const accordion = document.querySelector('#accordion')
const btnLoadText = document.querySelector('#loadText')
const docTitle = document.querySelector('#docTitle')
const docDate = document.querySelector('#docDate')
const docMeta = document.querySelector('#docMeta')
const btnSaveMeta = document.querySelector('#saveMetadata')
const annotationWindow = document.querySelector('#annotationWindow')
const helpText = document.querySelector('#helptext')
const btnEntity = document.querySelector('#btnEntity')
const btnAttr = document.querySelector('#btnAttr')
const mainWindow = document.querySelector('#mainWindow')
const spacyConsole = document.querySelector('#spacyConsole')
const sentimentConsole = document.querySelector('#sentimentConsole')
const modelConsole = document.querySelector('#modelConsole')
const modalHead = document.querySelector('#multiSelectHeader')
const modalSelect = document.querySelector('#elemSelect')
const modalSave = document.querySelector('#modalSave')
const exportName = document.querySelector('#exportName')
const exportSpacy = document.querySelector('#exportSpacy')
const exportSentiment = document.querySelector('#exportSentiment')
const exportModel = document.querySelector('#exportModel')


// Constants
const DEFAULT_HEAD = 0
const DEFAULT_DEP = '-'
const SUPPORTED_EXTS = new Set(['txt', 'xml'])

// Objects
class TagElement {

  constructor(word, innerText, index) {
    this.word = word
    this.innerText = innerText
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

  setChild(parentTag) {
    this.head = parentTag.index
    this.dep = 'CHILD'
  }

}

// State
let inputFile = null
let text = ''
let tags = []
let meta = {}
let modelEntries = []
let sentimentEntries = []

// Utils
function switchAccordion(oneIndex) {
  // TODO index bound check
  $('#accordion').children(`:nth-child(${oneIndex})`)
      .children(':nth-child(2)')
      .collapse('show')
}

// function reset() {
//   inputFile = null
//   text = ''
//   tags = []
//   meta = {}
//   modelEntries = []
// }

function createAnnotations() {
  const heads = tags.map(tag => tag.head)
  const deps = tags.map(tag => tag.dep)

  return {
    text: text,
    heads: heads,
    deps: deps
  }
}