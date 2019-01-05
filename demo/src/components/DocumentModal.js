import React, { Component } from "react";
import Document from './Document'
import { Modal, withStyles } from "@material-ui/core";

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
    open: this.props.document !== null
  }  

  render() {
    const { classes, document } = this.props
    return (
      <Modal
        aria-labelledby="document-title"
        aria-describedby="document-description"
        style={{alignItems:'center',justifyContent:'center'}}
        open={this.state.open}
        onClose={this.props.handleClose}  
      >
        <div style={{top: '10%', margin: 'auto'}} className={classes.paper}>
          <Document  document={document} />
        </div>
      </Modal>
    )
  }
}

export default withStyles(styles)(DocumentModal)