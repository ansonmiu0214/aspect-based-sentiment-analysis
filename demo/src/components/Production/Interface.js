import React, { Component } from "react";
import "../../App.css";
import Title from "../Title.js";
import Options from "./Options.js";
import Results from "./Results.js";
import DocumentList from '../DocumentList'
import DocumentAdder from './DocumentAdder'
import Grid from "@material-ui/core/Grid";
import Heading from "../Heading";
import BottomBar from "../BottomBar";
import { FileCopy, LibraryAdd, Search } from "@material-ui/icons";
import QueryView from "./QueryView";

class ProductionInterface extends Component {
  constructor(props) {
    super(props);
    this.updateResults = this.updateResults.bind(this);
  }

  state = {
    results: { entity: null, score: null, entries: [] },
    value: 0
  };

  bottomBarHandler = (event, value) => {
    this.setState({ value })
  }

  updateResults(results) {
    this.setState({ results });
  }

  render() {
    const { value } = this.state
    const actions = {
      'Documents': <FileCopy />,
      'Add': <LibraryAdd />,
      'Query': <Search />
    }
    return (
      // <div className="Production">
      <div>
        <Grid container justify="center">
          <Grid item xs={10}>
            {(value == 0) && <DocumentList heading="Processed Documents" apiOne="/absa/document" apiAll="/absa/documents" />}
            {(value == 1) && <DocumentAdder />}
            {(value == 2) && <QueryView />}
          </Grid>
        </Grid>


        {/* <Heading text="ABSA Demo" />
        <Grid container direction="row" justify="center" spacing={24}>
          <Grid style={{ padding: "0 5% 0 5%" }} item xs={4}>
            <Options updateResults={this.updateResults} />
          </Grid>
          <Grid style={{ padding: "0 5% 0 5%" }} item xs={8}>
            <Results results={this.state.results} />
          </Grid>
        </Grid> */}
        <BottomBar actions={actions} handleChange={this.bottomBarHandler} value={value} />
      </div>
    );
  }
}

export default ProductionInterface;
