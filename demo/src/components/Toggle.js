import React from "react";
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import { withStyles } from "@material-ui/core";

const StyledLabel = withStyles({
  label: {
    color: 'white'
  }
})(FormControlLabel)

function Toggle(props) {
  return (
    <FormGroup row>
      <StyledLabel
        control={
          <Switch
            checked={props.isProduction}
            onChange={props.toggleHandler}
            value="Production"
          />
        }
        label={props.isProduction ? "Production" : "Evaluation"}
      />
    </FormGroup>
  )
}

export default Toggle