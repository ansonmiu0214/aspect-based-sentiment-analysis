let entityIdxs = []

function onSelectEntity(event) {
  const start = entityIdxs[0]
  const end = entityIdxs.length > 1 ? entityIdxs[1] : entityIdxs[0]

  const entityString = parseString(start, end)
  
  if (selectedEntities.innerHTML != '') selectedEntities.innerHTML += ', ' 
  selectedEntities.innerHTML += entityString

  // Update tags
  for (let idx = start; idx <= end; ++idx) {
    tags[idx].setEntity()
  }

  entityEntries[entityString] = { start: start, end: end }
  
  // Add to dropdown
  const option = document.createElement('option')
  option.innerHTML = entityString
  entityDropdown.appendChild(option)

  entityCount.innerHTML = Number(entityCount.innerHTML) + 1

  btnSelectEntity.children[0].innerHTML = ''
  btnSelectEntity.disabled = true
}

function saveEntities(event) {
  if (Number(entityCount.innerHTML) == 0) {
    alert('No entities selected...')
    return
  }

  switchAccordion(4)
}

btnSelectEntity.addEventListener('click', onSelectEntity)
btnSaveEntities.addEventListener('click', saveEntities)