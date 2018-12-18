function exportSpacyData(event) {
  let name = exportName.nodeValue
  if (name.trim().length == 0) {
    alert('Export name required...')
    return
  }

  if (!name.endsWith('.json')) name += '.json'
  exportJSON(name, createAnnotations())
}

function exportSentimentData() {
  let name = exportName.nodeValue
  if (name.trim().length == 0) {
    alert('Export name required...')
    return
  }

  if (!name.endsWith('.json')) name += '.json'
  exportJSON(name, sentimentEntries)
}

function exportModelData() {
  let name = exportName.nodeValue
  if (name.trim().length == 0) {
    alert('Export name required...')
    return
  }

  if (!name.endsWith('.json')) name += '.json'
  exportJSON(name, modelEntries)
}

function exportJSON(name, obj) {
  const str = JSON.stringify(obj)

  // Create file
  const element = document.createElement('a')
  element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(str))
  element.setAttribute('download', name)

  // Download
  element.click()
}

exportSpacy.addEventListener('click', exportSpacyData)
exportSentiment.addEventListener('click', exportSentimentData)
exportModel.addEventListener('click', exportModelData)