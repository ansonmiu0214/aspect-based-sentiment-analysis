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
    marginBottom: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
})

function TPRow(props) {
  const { id, entity, attribute, expression, sentiment } = props
  const color = 'green'
  return (
    <TableRow key={id}>
      <TableCell style={{backgroundColor: color}}>{entity}</TableCell>
      <TableCell style={{backgroundColor: color}}>{attribute}</TableCell>
      <TableCell style={{backgroundColor: color}}>{expression}</TableCell>
      <TableCell style={{textAlign: 'right'}}>{sentiment}</TableCell>
    </TableRow>
  )
}

function NormalRow(props) {
  const { id, entity, attribute, expression, sentiment } = props
  return (
    <TableRow key={id}>
      <TableCell>{entity}</TableCell>
      <TableCell>{attribute}</TableCell>
      <TableCell>{expression}</TableCell>
      <TableCell style={{textAlign: 'right'}}>{sentiment}</TableCell>
    </TableRow>
  )
}

class TagTable extends Component {

  constructor(props) {
    super(props)
    this.tp = 'tp' in props ? props.tp : {}
    this.classes = props.classes
  }

  render() {
    const { classes, entities } = this.props
    const tp = this.tp
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
                  const idx = idOne * oneLength + idTwo * twoLength + idThree * threeLength

                  const isTruePositive = entity in tp && attribute in tp[entity]
                  return (
                    <NormalRow id={idx} entity={entity} attribute={attribute} expression={expression} sentiment={sentiment} />
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