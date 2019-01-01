import React, { Component } from 'react'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Typography from '@material-ui/core/Typography';
import Divider from "@material-ui/core/Divider";
import DocumentBody from './DocumentBody'
import TagTable from './TagTable'
import { withStyles } from '@material-ui/core';

const styles = theme => ({
  root: {
    width: '100%',
    // marginTop: theme.spacing.unit * 3,
    marginTop: '20px',
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
})

class Document extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { classes, document } = this.props
    const { id, components, entities, metadata } = document
    console.log(metadata)
    const { date, headline, title } = metadata
    
    return (
      <Card key={id} style={{maxHeight: '50vh', overflowY: 'auto'}}>
        <CardContent>
          <DocumentBody document={document} />
          <Divider />
          <TagTable entities={entities} />
        </CardContent>
      </Card>
    )
  }
}

export default withStyles(styles)(Document)