import React, { Component } from 'react'
import CircularProgress from '@material-ui/core/CircularProgress'
import { withStyles, Typography } from "@material-ui/core";

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
    const { text } = this.props
    return (
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div><CircularProgress color="secondary" className={this.classes.progress}/></div>
        {
          (text !== undefined) &&
            <div>
              <Typography color="textSecondary" variant="h5">
                {text}
              </Typography>
            </div>
        }
      </div>
    )
  }
}

export default withStyles(styles)(Loader)