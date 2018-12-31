import React, { Component } from "react";
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import { withStyles } from "@material-ui/core";

const styles = theme => ({
  label: {
    color: 'white'
  }
})

const StyledLabel = withStyles({
  label: {
    color: 'white'
  }
})(FormControlLabel)
  
class Toggle extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <FormGroup row>
        <StyledLabel
          control={
            <Switch
              checked={this.props.isProduction}
              onChange={this.props.toggleHandler}
              value="Production"
            />
          }
          label={this.props.isProduction ? "Production" : "Evaluation"}
        />
      </FormGroup>
    )
  }

}

export default Toggle
// export default withStyles(styles)(Toggle)