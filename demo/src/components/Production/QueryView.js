import React, { Component } from "react";
import Grid from "@material-ui/core/Grid";
import Options from './Options'
import Results from './Results'
import Heading from "../Heading";
import Loader from "../Loader";

class QueryView extends Component {
  
  constructor(props) {
    super(props)
    this.updateResults = this.updateResults.bind(this)
    this.setLoading = this.setLoading.bind(this)
  }

  state = {
    results: { entity: null, score: null, entries: [] },
    loading: false
  }

  setLoading(loading) {
    this.setState({ loading })
  }
  
  updateResults(results) {
    this.setState({ results });
  }

  render() {
    const { loading, results } = this.state
    return (
      <>
      <Heading text="Query Handler" />
      <Grid container justify="center" spacing={24}>
        <Grid item xs={4}>
          <Options setLoading={this.setLoading} updateResults={this.updateResults} />
        </Grid>
        <Grid item xs={8} style={{marginBottom: '50px'}}>
          {loading && <Loader />}
          {!loading && results != [] && <Results results={results} />}
        </Grid>
      </Grid>
      </>
    )
  }

}

export default QueryView