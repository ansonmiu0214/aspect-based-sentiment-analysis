// // Constants
// const DEFAULT_HEAD = 0
// const DEFAULT_DEP = '-'

// // DOM
// const fileUpload = document.getElementById('fileUpload')
// const btnLoadDoc = document.getElementById('loadDocument')
// const annotationWindow = document.getElementById('annotationWindow')

// const btnEnt = document.getElementById('btnEntity')
// const btnAttr = document.getElementById('btnAttribute')
// const btnSent = document.getElementById('btnSentiment')

// const textArea = document.getElementById('textArea')
// const instructions = document.getElementById('helptext')
// const exportName = document.getElementById('exportName')
// const exportButton = document.getElementById('exportJSON')
// const consoleWindow = document.getElementById('console')

// const modal = document.getElementById('')
// const modalHead = document.getElementById('multiSelectHeader')
// const modalSelect = document.getElementById('elemSelect')
// const modalSave = document.getElementById('modalSave')

// // Objects
// class TagElement {

//   constructor(word, index) {
//     this.word = word
//     this.index = index
//     this.head = DEFAULT_HEAD
//     this.dep = DEFAULT_DEP
//   }

//   setEntity() {
//     this.head = this.index
//     this.dep = 'ENTITY'
//   }

//   setAttribute(entityTag) {
//     this.head = entityTag.index
//     this.dep = 'ATTRIBUTE'
//   }

//   setSentiment(attributeTag) {
//     this.head = attributeTag.index
//     this.dep = 'SENTIMENT'
//   }

//   setChild(parentTag) {
//     this.head = parentTag.index
//     this.dep = 'CHILD'
//   }

// }

// /**
//  * Global state
//  * (mode, text, tags)
//  */

// var text = ""
// const tags = []
// var selectedIdxs = []
// var entity = null
// var attribute = null
// var currMode = 'entity'

// const modes = {
//   'entity': {
//     setup: () => {
//       instructions.innerHTML = 'Select ENTITY.'
//     },
//     btn: btnEnt,
//     singleHandler: (tagIdx) => {
//       const entityTag = tags[tagIdx]
//       entityTag.setEntity()
//       entity = entityTag
//     },
//     multiHandler: (startIdx, endIdx, primaryIdx) => {
//       const entityTag = tags[primaryIdx]
//       for (let idx = startIdx; idx <= endIdx; ++idx) {
//         if (idx != primaryIdx) tags[idx].setChild(entityTag)
//       }
//       entityTag.setEntity()
//       entity = entityTag
//     },
//     nextMode: () => {
//       btnEnt.children[0].innerHTML = ''
//       btnEnt.disabled = true
//       selectedIdxs = []
//       currMode = 'attribute'
//     }
//   },
//   'attribute': {
//     setup: () => {
//       instructions.innerHTML = `Entity OK. Select ATTRIBUTE for '${entity.word}'`
//     },
//     btn: btnAttr,
//     singleHandler: (tagIdx) => {
//       const attrTag = tags[tagIdx]
//       attrTag.setAttribute(entity)
//       attribute = attrTag
//     },
//     multiHandler: (startIdx, endIdx, primaryIdx) => {
//       const attrTag = tags[primaryIdx]
//       for (let idx = startIdx; idx <= endIdx; ++idx) {
//         if (idx != primaryIdx) tags[idx].setChild(attrTag)
//       }
//       attrTag.setAttribute(entity)
//       attribute = attrTag
//     },
//     nextMode: () => {
//       btnAttr.children[0].innerHTML = ''
//       btnAttr.disabled = true
//       selectedIdxs = []
//       currMode = 'sentiment'
//     }
//   }, 
//   'sentiment': {
//     setup: () => {
//       instructions.innerHTML = `Entity OK. Attribute OK. Select SENTIMENT for '${attribute.word}' of '${entity.word}'`
//     },
//     btn: btnSent,
//     singleHandler: (tagIdx) => {
//       const sentTag = tags[tagIdx]
//       sentTag.setSentiment(attribute)
//       entity = null
//       attribute = null
//     },
//     multiHandler: (startIdx, endIdx, primaryIdx) => {
//       const sentTag = tags[primaryIdx]
//       for (let idx = startIdx; idx <= endIdx; ++idx) {
//         if (idx != primaryIdx) tags[idx].setChild(sentTag)
//       }
//       sentTag.setSentiment(attribute)
//       entity = null
//       attribute = null
//     },
//     nextMode: () => {
//       btnSent.children[0].innerHTML = ''
//       btnSent.disabled = true
//       selectedIdxs = []
//       currMode = 'entity'
//       printAnnotations()
//     }
//   }
// }

// /**
//  * Event handlers
//  */

// function textSelection(event) {
//   // Ignore if nothing selected
//   const selection = window.getSelection()
//   if (!selection) return

//   // Ignore if no text selected
//   if (selection.rangeCount == 0) return
//   const range = selection.getRangeAt(0)

//   // Ignore if text selection is outside window
//   if (range.startContainer.parentNode.classList != 'word') return

//   const startIdx = range.startContainer.parentNode.getAttribute('data-idx')
//   const endIdx = range.endContainer.parentNode.getAttribute('data-idx')
//   const count = endIdx - startIdx + 1

//   // Enable the corresponding button and update badge
//   modes[currMode].btn.disabled = false
//   modes[currMode].btn.children[0].innerHTML = count

//   selectedIdxs = (startIdx == endIdx) ? [startIdx] : [startIdx, endIdx]
// }

// function onTagClick(event) {
//   if (selectedIdxs.length == 1) {
//     modes[currMode].singleHandler(selectedIdxs[0])
//     modes[currMode].nextMode()
//     modes[currMode].setup()
//   } else {
//     // Initialise modal for selection
//     initSelectionModal()
//     $('#multiSelectModal').modal('show')
//   }
// }

// function initSelectionModal() {
//   modalHead.innerHTML = `Multi-Word: ${currMode.toUpperCase()}`
//   modalSelect.innerHTML = ''

//   const [startIdx, stopIdx] = selectedIdxs
//   for (let idx = startIdx; idx <= stopIdx; ++idx) {
//     const option = document.createElement('option')
//     option.innerHTML = `${idx}: ${tags[idx].word}`
//     modalSelect.appendChild(option)
//   }
// }

// function onModalSaveClick(event) {
//   const primaryIdx = parseInt(modalSelect.value.split(':')[0]) 
//   const [startIdx, stopIdx] = selectedIdxs
//   $('#multiSelectModal').modal('hide')
//   modes[currMode].multiHandler(startIdx, stopIdx, primaryIdx)
//   modes[currMode].nextMode()
//   modes[currMode].setup()
// }

// function loadText(event) {
//   text = textArea.value

//   // Reset annotation window
//   annotationWindow.innerHTML = ''

//   if (text == '') return

//   // Call spaCy to parse tokens
//   $.ajax({
//     type: 'POST',
//     url: './tokenise',
//     data: JSON.stringify({ text: text }),
//     contentType: 'application/json',
//     success: data => handleTokens(data.data)
//   })
// }

// function handleTokens(words) {
//   let spaceOffset = 0
//   let space = ' '
//   for (let idx = 0; idx < words.length; ++idx) {
//     const word = words[idx]
//     if (word.trim().length == 0) {
//       ++spaceOffset
//       space += word
//       continue
//     }

//     const correctIdx = idx - spaceOffset
//     const tag = new TagElement(word, correctIdx)

//     const spanElement = document.createElement('span')
//     spanElement.classList.add('word')
//     spanElement.innerText = space + word
//     spanElement.setAttribute('data-idx', correctIdx)
//     space = ' '

//     tags.push(tag)
//     annotationWindow.appendChild(spanElement)    
//   }

//   console.log(tags)
//   modes[currMode].setup()
// }

// function printAnnotations() {
//   const annotations = createAnnotations()
//   consoleWindow.innerHTML = `<pre>${JSON.stringify(annotations, null, 2)}</pre>`
// }

// function createAnnotations() {
//   const heads = tags.map(tag => tag.head)
//   const deps = tags.map(tag => tag.dep)

//   return {
//     text: text,
//     heads: heads,
//     deps: deps
//   }
// }

// function exportJSON(event) {
//   // Get filename
//   let name = exportName.value
//   if (name == '') {
//     alert('Export name required.')
//     return
//   }

//   const annotations = JSON.stringify(createAnnotations())
//   if (!name.endsWith('.json')) name += '.json'

//   // Create file
//   const element = document.createElement('a')
//   element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(annotations))
//   element.setAttribute('download', name)
//   element.click()
// }

// function readFile(event) {
//   const file = fileUpload.files[0]
//   if (!file) return

//   const fileReader = new FileReader()
//   fileReader.onload = event => textArea.value = event.target.result
//   fileReader.onerror = _ => textArea.value = 'Error reading file'

//   fileReader.readAsText(file, 'utf-8')
// }

// function init() {
//   // loadText()
//   // updateHelpText()

//   btnLoadDoc.addEventListener('click', loadText())

//   // Assign handler for text selection
//   document.onmouseup = textSelection

//   // Actual tagging buttons
//   btnEnt.addEventListener('click', onTagClick)
//   btnAttr.addEventListener('click', onTagClick)
//   btnSent.addEventListener('click', onTagClick)

//   // Modal save button
//   modalSave.addEventListener('click', onModalSaveClick)

//   // Export button
//   exportButton.addEventListener('click', exportJSON)

//   // File upload
//   fileUpload.addEventListener('change', readFile)  
// }

// init()