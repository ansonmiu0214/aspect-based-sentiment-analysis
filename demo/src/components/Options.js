import React, { Component } from "react";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import axios from "axios";

class Options extends Component {
  constructor(props) {
    super(props);
    this.state = { entity: "" };

    this.search = this.search.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  search() {
    axios
      .get("/docs", {
        params: { entity: this.state.entity }
      })
      .then(r => this.props.updateDocuments(r.data))
      .catch(e => console.log(e));
  }

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value
    });
  };

  render() {
    return (
      <div>
        <TextField
          label="Entity"
          value={this.state.name}
          onChange={this.handleChange("entity")}
          margin="normal"
        />
        <Button variant="contained" onClick={this.search}>
          Search
        </Button>
      </div>
    );
  }
}

export default Options;
