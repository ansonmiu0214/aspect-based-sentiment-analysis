import React, { Component } from "react";
import "../../App.css";
import Title from "../Title.js";
import Options from "../Options.js";
import Results from "../Results.js";
import Grid from "@material-ui/core/Grid";

class ProductionInterface extends Component {

  state = {
    results: { entity: null, score: null, entries: [] },
  }

  render() {
    return (
      <div className="Production">
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

export default ProductionInterface