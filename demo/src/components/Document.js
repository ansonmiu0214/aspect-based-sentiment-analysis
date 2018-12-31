import React, { Component } from 'react'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import CardActions from '@material-ui/core/CardActions';
import Typography from '@material-ui/core/Typography';
import Divider from "@material-ui/core/Divider";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import { withStyles } from '@material-ui/core';

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
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
    const { classes } = this.props
    const { id, components, entities, metadata } = this.props.document
    console.log(metadata)
    const { date, headline, title } = metadata
    
    return (
      <Card key={id} style={{maxHeight: '50vh', overflowY: 'auto'}}>
        <CardContent>
          <Typography color="textSecondary" gutterBottom>
            Document #{id}
          </Typography>
          <Typography color="textSecondary" gutterBottom>
            {date}
          </Typography>
          <Typography color="textSecondary" gutterBottom>
            {title}
          </Typography>
          <Typography color="textSecondary" gutterBottom>
            {headline}
          </Typography>
          {
            components.map(({ text }) => {
              return <Typography component="p" style={{marginBottom: '5px', lineHeight: '1.5rem'}}>{text}</Typography>
            })
          }
          <Divider />

          <Table className={classes.root}>
            <TableHead>
              <TableRow>
                <TableCell>Entity</TableCell>
                <TableCell>Attribute</TableCell>
                <TableCell>Expression</TableCell>
                <TableCell>Sentiment</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {
                entities.map(({ entity, attributes }, idOne) =>
                  attributes.map(({ attribute, expressions }, idTwo) =>
                    expressions.map(({ expression, sentiment }, idThree) => {
                      const threeLength = expressions.length
                      const twoLength = attributes.length + threeLength
                      const oneLength = entities.length + twoLength
                      const idx = idOne * oneLength + idTwo * twoLength + idThree * this.UNSAFE_componentWillMount
                      
                      return (
                        <TableRow key={idx}>
                          <TableCell>{entity}</TableCell>
                          <TableCell>{attribute}</TableCell>
                          <TableCell>{expression}</TableCell>
                          <TableCell>{sentiment}</TableCell>
                        </TableRow>
                      )
                    })
                  )
                )
              }
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    )
  }
}

export default withStyles(styles)(Document)