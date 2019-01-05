import React, { Component } from 'react'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import Typography from '@material-ui/core/Typography';
import Divider from "@material-ui/core/Divider";
import DocumentBody from './DocumentBody'
import TagTable from './TagTable'
import { withStyles } from '@material-ui/core';

class Document extends Component {

  constructor(props) {
    super(props)
    this.notModal = 'notModal' in props
  }

  render() {
    const { document } = this.props
    const { id, entities } = document
    
    return (
      <Card key={id} style={this.notModal ? {} : {maxHeight: '80vh', overflowY: 'auto'}}>
        <CardContent>
          <DocumentBody document={document} />
          <Divider />
          <TagTable entities={entities} />
        </CardContent>
      </Card>
    )
  }
}

export default Document