import React, { Component } from "react";
import Document from './Document'
import { Modal, withStyles } from "@material-ui/core";
import Loader from "./Loader";
import axios from "axios";

const styles = theme => ({
  paper: {
    position: 'relative',
    width: '80vw',
    backgroundColor: theme.palette.background.paper,
    boxShadow: theme.shadows[5],
    padding: theme.spacing.unit * 4,
    outline: 'none',
  },
});

class DocumentModal extends Component {
  constructor(props) {
    super(props)
    this.classes = props.classes
  }

  state = {
    open: this.props.documentId !== null,
    loading: true,
    document: null
  }
  
  componentDidMount() {
    axios.get(`${this.props.api}?id=${this.props.documentId}`)
      .then(({ data }) => {
        this.setState({ loading: false, document: data })
      })
      .catch(error => {
        console.error(error)
        this.setState({ loading: false })
      })
  }

  render() {
    const { loading, document } = this.state
    const { classes } = this.props
    return (
      <Modal
        aria-labelledby="document-title"
        aria-describedby="document-description"
        style={{alignItems:'center',justifyContent:'center'}}
        open={this.state.open}
        onClose={this.props.handleClose}  
      >
        {   
          <div style={{top: '10%', margin: 'auto'}} className={classes.paper}>
            { loading && <Loader text="Fetching document..." />}
            { !loading && <Document  document={document} />}
          </div>
        }
      </Modal>
    )
  }
}

export default withStyles(styles)(DocumentModal)