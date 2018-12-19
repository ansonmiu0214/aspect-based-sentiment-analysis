function fileUploadListener(event) {
  const file = fileUpload.files[0]
  if (!file) {
    alert('No file detected...')
    return
  }

  const ext = file.name.substring(file.name.length - 3)
  if (!SUPPORTED_EXTS.has(ext)) {
    alert('Unsupported file extension...')
    return
  }

  inputFile = ext
  console.log(inputFile)

  const loader = document.querySelector('#loaderOne')
  loader.classList.add('active')

  const fileReader = new FileReader()
  fileReader.onload = _ => {
    textArea.value = fileReader.result.toString()
    loader.classList.remove('active')
  }

  fileReader.onerror = _ => {
    loader.classList.remove('active')
    alert('Error reading file...')
  }

  fileReader.readAsText(file, 'utf-8')
}

fileUpload.addEventListener('change', fileUploadListener)

function loadText(event) {
  text = textArea.value
  const request = { text: text }

  if (inputFile != null) request['extension'] = inputFile

  const loader = document.querySelector('#loaderOne')
  loader.classList.add('active')

  console.log(request)

  $.ajax({
    type: 'POST',
    url: './tokenise',
    data: JSON.stringify(request),
    contentType: 'application/json',
    success: (response) => {
      loader.classList.remove('active')
      switchAccordion(2)
      
      console.log(response)
      const { data } = response

      if ('meta' in response) initMetadata(response['meta'])

      initWindow(entityWindow, data)
      initWindow(mainWindow, data) 
    },
    error: (error) => {
      loader.classList.remove('active')
      alert(JSON.stringify(error))
    }
  })
}

btnLoadText.addEventListener('click', loadText)