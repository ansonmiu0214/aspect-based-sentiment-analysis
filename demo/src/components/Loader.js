import React, { Component } from 'react'
import CircularProgress from '@material-ui/core/CircularProgress'
import { withStyles } from "@material-ui/core";

const styles = theme => ({
  progress: {
    margin: theme.spacing.unit * 2
  },
})

class Loader extends Component {
  constructor(props) {
    super(props)
    this.classes = props.classes
  }

  render() {
    return (
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div><CircularProgress color="secondary" className={this.classes.progress}/></div>
      </div>
    )
  }
}

export default withStyles(styles)(Loader)