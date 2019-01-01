import React, { Component } from 'react'
import PropTypes from 'prop-types';
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import axios from 'axios'
import DeleteSweepIcon from '@material-ui/icons/DeleteSweep'
import Heading from '../Heading'
import Loader from '../Loader'
import DocumentModal from '../DocumentModal';

const styles = theme => ({
  title: {
    fontSize: 14
  },
  pos: {
    marginBottom: 12,
  },
  fab: {
    margin: theme.spacing.unit,
    position: 'fixed',
    bottom: theme.spacing.unit * 8,
    right: theme.spacing.unit * 12,
  },
})

class DocumentList extends Component {
  constructor(props) {
    super(props)
    this.classes = props.classes
    this.updateDocuments = this.updateDocuments.bind(this)
    this.deleteAll = this.deleteAll.bind(this)
    this.hideDocument = this.hideDocument.bind(this)
  }

  state = {
    loading: true,
    documents: [],
    showDocument: null,
  }

  componentDidMount() {
    this.updateDocuments()
  }

  updateDocuments() {
    axios.get("/test/documents")
    .then(({ data }) => {
      this.setState({ loading: false })
      this.handleDocuments(data)
    })
    .catch(error => {
      this.setState({ loading: false })
      console.error(error)
    })
  }

  handleDocuments(documents) {
    this.setState({ documents })
  }

  showDocument(event, documentId) {
    axios.get(`/test/document?id=${documentId}`)
      .then(({ data }) => {
        this.setState({ showDocument: data })
      })
      .catch(error => {
        console.error(error)
      })
  }

  hideDocument() {
    this.setState({ showDocument: null })
  }

  deleteAll(event) {
    this.setState({ loading: true })
    axios.delete("/test/documents")
      .then(_ => this.updateDocuments())
      .catch(error => {
        this.setState({ loading: false })
        console.error(error)
      })
  }

  render() {
    const { classes } = this 
    const { documents, loading, showDocument } = this.state
    return (
      <>
      <Heading text="Test Set Documents" />
      {loading && <Loader classes={this.classes} />}
      {!loading && 
        <div>
          {documents.map(element => {
            const { id, metadata } = element
            const { date, title, headline } = metadata
            return (
              <Card key={id}>
                <CardContent>
                <Typography className={classes.title} color="textSecondary" gutterBottom>
                  {date}
                </Typography>
                <Typography variant="h5" component="h2">
                  {title}
                </Typography>
                {/* <Typography className={classes.pos} color="textSecondary">
                  {Object.keys(others).map(key => `${key}: ${others[key]}`).join('<br />')}
                </Typography> */}
                <Typography component="p">
                  {headline}
                </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={event => this.showDocument(event, id)}>Preview</Button>
                </CardActions>
              </Card>
            )
          })}
          {
            (showDocument !== null) && <DocumentModal document={showDocument} handleClose={this.hideDocument} />
          }
          <Button variant="fab" color="secondary" aria-label="Add" className={classes.fab} onClick={this.deleteAll}>
            <DeleteSweepIcon />
          </Button>
        </div>
      }
      </>
    )
  }
}

DocumentList.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DocumentList)