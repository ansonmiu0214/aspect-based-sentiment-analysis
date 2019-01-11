import React from 'react'
import Typography from '@material-ui/core/Typography'

function Heading(props) {
  return (
    <Typography variant="h3" component="h3" style={{marginTop: '50px', marginBottom: '50px'}} align="center" gutterBottom>
      {props.text}
    </Typography>
  )
}

export default Heading