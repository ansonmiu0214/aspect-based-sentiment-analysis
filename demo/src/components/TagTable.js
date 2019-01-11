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

function NormalRow(props) {
  const { entity, attribute, expression, sentiment } = props
  return (
    <TableRow>
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

  comparatorFor = field => (elem1, elem2) => {
    const first = elem1[field]
    const second = elem2[field]

    return first == second ? 0 : (first < second ? -1 : 1)
  }

  render() {
    const { classes, entities } = this.props
    const { comparatorFor } = this
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
            entities.sort(comparatorFor('entity')).map(({ entity, attributes }, idOne) => 
              attributes.sort(comparatorFor('attribute')).map(({ attribute, expressions }, idTwo) => 
                expressions.sort(comparatorFor('expression')).map(({ expression, sentiment }, idThree) => {
                    const threeLength = expressions.length
                    const twoLength = attributes.length + threeLength
                    const oneLength = entities.length + twoLength
                    const idx = idOne * oneLength + idTwo * twoLength + idThree * threeLength

                    return <NormalRow key={idx} entity={entity} attribute={attribute} expression={expression} sentiment={sentiment} />
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