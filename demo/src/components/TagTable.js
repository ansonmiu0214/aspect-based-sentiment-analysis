import React, { Component } from 'react'
import { withStyles } from '@material-ui/core';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

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

class TagTable extends Component {

  constructor(props) {
    super(props)
    this.classes = props.classes
  }

  render() {
    const { classes, entities } = this.props
    return (
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
                      <TableCell align="right">{sentiment}</TableCell>
                    </TableRow>
                  )
                })
              )
            )
          }
        </TableBody>
      </Table>
    )
  }

}

export default withStyles(styles)(TagTable)