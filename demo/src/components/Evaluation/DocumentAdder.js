import React, { Component } from 'react'
import Button from "@material-ui/core/Button";
import CloudUploadIcon from "@material-ui/icons/CloudUpload";
import Grid from "@material-ui/core/Grid";
import Document from '../Document'
import Heading from '../Heading'
import Loader from '../Loader'
import axios from 'axios'

class TestAdder extends Component {
  constructor(props) {
    super(props)
    this.docInput = React.createRef()
    this.jsonInput = React.createRef()
    this.submitHandler = this.submitHandler.bind(this)
  }

  submitHandler(event) {
    event.preventDefault()

    if (!this.docInput.current || !this.jsonInput.current) return

    const formData = new FormData()
    formData.append("document", this.docInput.current.files[0])
    formData.append("tags", this.jsonInput.current.files[0])

    this.props.toggleLoading()

    axios.post('/test/document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(({ data }) => {
      this.props.requestDocument(data.documentId)
    }).catch(error => {
      this.props.toggleLoading()
      console.error(error)
    })
  }

  render() {
    return (
      <Grid
        container
        direction="column"
        spacing={16}
        justify="center"
        alignItems="center"
      >
        <Grid item>
          <input
            accept=".xml, .txt"
            id="document-upload"
            multiple
            type="file"
            style={{ display: "none" }}
            ref={this.docInput}
          />
          <label htmlFor="document-upload">
            <Button variant="contained" color="default" component="span">
              Upload Document
              <CloudUploadIcon style={{ marginLeft: "0.25em" }} />
            </Button>
          </label>
        </Grid>
        <Grid item>
          <input
            accept=".json"
            id="json-upload"
            multiple
            type="file"
            style={{ display: "none" }}
            ref={this.jsonInput}
          />
          <label htmlFor="json-upload">
            <Button variant="contained" color="default" component="span">
              Upload JSON Tags
              <CloudUploadIcon style={{ marginLeft: "0.25em" }} />
            </Button>
          </label>
        </Grid>
        <Grid item>
          <Button
            variant="contained"
            color="default"
            component="span"
            onClick={event => this.submitHandler(event)}
          >
            Submit
          </Button>
        </Grid>
      </Grid>
    )
  }
}

class DocumentAdder extends Component {
  constructor(props) {
    super(props)
    this.toggleLoading = this.toggleLoading.bind(this)
    this.requestDocument = this.requestDocument.bind(this)
  }

  state = {
    loading: false,
    document: null
  }

  toggleLoading() {
    this.setState(prevState => ({ loading: !prevState.loading }))
  }

  requestDocument(documentId) {
    axios.get(`/test/document?id=${documentId}`)
      .then(response => this.setState({ document: response.data, loading: false }))
      .catch(console.error)
  }

  render() {
    const { document, loading } = this.state
    return (
      <>
      <Heading text="Add Test Document" />
      {loading && <Loader text="Adding test document..."/>}
      {!loading && 
        <Grid container direction="row" justify="center" spacing={24}>
          <Grid style={{ padding: "0 5% 10% 5%" }} item xs={4}>
            <TestAdder toggleLoading={this.toggleLoading} requestDocument={this.requestDocument} />
          </Grid>
          <Grid style={{ padding: "0 5% 10% 5%" }} item xs={8}>
            {(document !== null) && <Document document={document} notModal/>}
          </Grid>
        </Grid>
      }
      </>
    )
  }
}

export default DocumentAdder