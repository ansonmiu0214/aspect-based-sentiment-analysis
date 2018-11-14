import React, { Component } from "react";
import Title from "./components/Title.js";
import Options from "./components/Options.js";
import Results from "./components/Results.js";
import Grid from "@material-ui/core/Grid";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { results: { entity: null, score: null, entries: [] } };
    this.updateResults = this.updateResults.bind(this);
  }

  updateResults(results) {
    this.setState({ results });
  }

  render() {
    return (
      <div className="App">
        <Title />
        <Grid container direction="row" justify="center" spacing={24}>
          <Grid style={{ padding: "0 5% 0 5%" }} item xs={4}>
            <Options updateResults={this.updateResults} />
          </Grid>
          <Grid style={{ padding: "0 5% 0 5%" }} item xs={8}>
            <Results results={this.state.results} />
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default App;
