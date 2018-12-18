function initMetadata(metadata) {
  for (let key in metadata) {
    const val = metadata[key]
    if (key == 'title') {
      docTitle.value = val
    } else if (key == 'date') {
      docDate.value = val
    } else {
      if (docMeta.value.length > 0) docMeta.value += ','
      docMeta.value += `${key}=${val}`
    }
  }
}

function saveMetadata(event) {
  meta = {}

  meta['title'] = docTitle.value
  exportName.value = meta['title']

  meta['date'] = docDate.value

  if (docMeta.value.length > 0) {
    const pairs = docMeta.value.split(',')

    for (let pair of pairs) {
      const [key, val] = pair.split('=')
      meta[key] = val
    }
  }

  annotationWindow.innerHTML = 'Nothing selected: highlight an expression from the window below.'
  switchAccordion(3)
}

btnSaveMeta.addEventListener('click', saveMetadata)