import React, { Component } from "react";
import MenuBar from "./components/MenuBar.js";
import ProductionInterface from "./components/Production/Interface";
import EvaluationInterface from "./components/Evaluation/Interface";

class App extends Component {
  constructor(props) {
    super(props);
    this.toggleHandler = this.toggleHandler.bind(this);
  }

  state = {
    isProduction: true
  };

  toggleHandler() {
    this.setState(prevState => ({
      isProduction: !prevState.isProduction
    }));
  }

  render() {
    return (
      <div className="App">
        <MenuBar
          isProduction={this.state.isProduction}
          toggleHandler={this.toggleHandler}
        />
        {this.state.isProduction && <ProductionInterface />}
        {!this.state.isProduction && <EvaluationInterface />}
      </div>
    );
  }
}

export default App;
