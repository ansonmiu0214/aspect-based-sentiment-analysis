import React, { Component } from 'react'
import PropTypes from 'prop-types';
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import CardActions from '@material-ui/core/CardActions';
import Button from '@material-ui/core/Button';
import { withStyles, Grid, Tooltip } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import axios from 'axios'
import DeleteSweepIcon from '@material-ui/icons/DeleteSweep'
import Heading from './Heading'
import Loader from './Loader'
import DocumentModal from './DocumentModal';

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
    axios.get(this.props.apiAll)
    .then(({ data }) => {
      this.setState({ loading: false })
      this.handleDocuments(data)
    })
    .catch(error => {
      console.error(error)
      this.setState({ loading: false })
    })
  }

  handleDocuments(documents) {
    this.setState({ documents })
  }

  showDocument(event, documentId) {
    this.setState({ showDocument: documentId })
  }

  hideDocument() {
    this.setState({ showDocument: null })
  }

  deleteAll(event) {
    this.setState({ loading: true })
    axios.delete(this.props.apiAll)
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
      <Heading text={this.props.heading} />
      {loading && <Loader classes={this.classes} />}
      {!loading && 
        <Grid container spacing={24}>
          {documents.map(element => {
            const { id, metadata } = element
            const { date, title, headline } = metadata
            return (
              <Grid key={id} item xs={12} lg={6}>
                <Card>
                  <CardContent>
                  <Typography className={classes.title} color="textSecondary" gutterBottom>
                    {date}
                  </Typography>
                  <Typography variant="h5" component="h2">
                    {title}
                  </Typography>
                  <Typography component="p">
                    {headline}
                  </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small" onClick={event => this.showDocument(event, id)}>Preview</Button>
                  </CardActions>
                </Card>
              </Grid> 
            )
          })}
          {
            (showDocument !== null) && <DocumentModal documentId={showDocument} api={this.props.apiOne} handleClose={this.hideDocument} />
          }
          <Tooltip title="Delete All" placement="top">
            <Button variant="fab" color="secondary" aria-label="Add" className={classes.fab} onClick={this.deleteAll}>
              <DeleteSweepIcon />
            </Button>
          </Tooltip>
        </Grid>
      }
      </>
    )
  }
}

DocumentList.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DocumentList)