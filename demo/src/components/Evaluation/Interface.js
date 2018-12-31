import React, { Component } from "react";
import BottomBar from "./BottomBar";
import DocumentList from './DocumentList'
import DocumentAdder from './DocumentAdder'
import Evaluator from './Evaluator'
import Grid from '@material-ui/core/Grid';

class EvaluationInterface extends Component {

  constructor(props) {
    super(props)
    this.bottomBarHandler.bind(this)
  }

  state = {
    value: 0
  }

  bottomBarHandler = (event, value) => {
    this.setState({ value })
  }

  render() {
    const { value } = this.state
    return (
      <>
      <Grid container justify="center">
        <Grid item xs={10}>
          {(value == 0) && <DocumentList />}
          {(value == 1) && <DocumentAdder />}
          {(value == 2) && <Evaluator />}
        </Grid>
      </Grid>
      <BottomBar handleChange={this.bottomBarHandler} value={this.state.value} />
      </>
    )
  }
}

export default EvaluationInterface