import React, { Component } from "react";
import Heading from '../Heading'
import Loader from '../Loader'
import axios from 'axios'
import { Paper, Typography, Divider } from "@material-ui/core";

class Scores extends Component {
  
  constructor(props) {
    super(props)
  }

  render() {
    const { result, breakdown } = this.props
    return (
      <Paper style={{padding: '20px'}}>
        <Typography color="textSecondary" gutterBottom>
          Average F1 Score
        </Typography>
        <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
          {Number(result).toFixed(3)}
        </Typography>
        <Divider />
        <div style={{marginTop: '20px'}}>
          {
            breakdown.map(({ id, score }) => {
              return (
                <>
                <Typography color="textSecondary" gutterBottom>
                  Document #{id}
                </Typography>
                <Typography variant="h4" component="h2" style={{marginBottom: '20px'}}>
                  {Number(score).toFixed(3)}
                </Typography>
                </>
              )
            })
          }
        </div>
      </Paper>
    )
  }
}

class Evaluator extends Component {

  constructor(props) {
    super(props)
  }

  state = {
    result: null,
    breakdown: null,
    loading: true,
  }

  componentWillMount() {
    axios.get('/test')
      .then(({ data }) => {
        const { result, breakdown } = data
        this.setState({ loading: false, result: result, breakdown: breakdown })
      })
  }

  render() {
    const { result, breakdown, loading } = this.state
    return (
      <>
      <Heading text="Model Evaluation" />
      {loading && <Loader />}
      {!loading && <Scores result={result} breakdown={breakdown}/>}
      </>
    )

  }

}

export default Evaluator