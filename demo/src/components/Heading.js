import React, { Component } from 'react'
import Typography from '@material-ui/core/Typography'

class Heading extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <Typography variant="h3" component="h3" style={{marginTop: '50px', marginBottom: '50px'}} align="center" gutterBottom>
        {this.props.text}
      </Typography>
    )
  }
}

export default Heading