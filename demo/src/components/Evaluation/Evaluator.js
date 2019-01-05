import React, { Component } from "react";
import Heading from '../Heading'
import Loader from '../Loader'
import axios from 'axios'
import { Paper, Typography, Grid } from "@material-ui/core";
import { withStyles } from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import TagTable from "../TagTable";

const panelStyle = theme => ({
  heading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '33.33%',
    flexShrink: 0,
  },
  // secondaryHeading: {
  //   fontSize: theme.typography.pxToRem(15),
  //   flexBasis: '10%',
  //   flexShrink: 0,
  //   color: theme.palette.text.secondary,
  // },
  numberHeading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '20%',
    flexShrink: 0,
    color: theme.palette.text.secondary,
  }
});

function LabelledTagTable(props) {
  const { title, entities } = props
  const tp = 'tp' in props ? props.tp : {}
  return (
    <>
      <Typography style={{textAlign: 'center'}} variant="h5" component="h5" gutterBottom>
        {title}
      </Typography>
      <TagTable entities={entities} tp={tp} />
    </>
  )
}

class Entry extends Component {
  constructor(props) {
    super(props)
    this.classes = props.classes
  }

  render() {
    const { breakdown, handleChange, expanded, classes, dp } = this.props
    const { id, score, ent_f1, attr_f1, model, truth, tp } = breakdown
    console.log(Object.keys(tp))
    return (
      <ExpansionPanel expanded={expanded === id} onChange={handleChange(id)}>
        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
          <Typography className={classes.heading}>Document #{id}</Typography>
          <Typography className={classes.numberHeading}>Combined F-Score: {Number(score).toFixed(dp)}</Typography>
          <Typography className={classes.numberHeading}>Entity F-Score: {Number(ent_f1).toFixed(dp)}</Typography>
          <Typography className={classes.numberHeading}>Attribute F-Score: {Number(attr_f1).toFixed(dp)}</Typography>
        </ExpansionPanelSummary>
        <ExpansionPanelDetails>
          <Grid container spacing={24}>
            <Grid item xs={12} lg={6}>
              <LabelledTagTable title="Model Output" entities={model} tp={tp} />
            </Grid>
            <Grid item xs={12} lg={6}>
              <LabelledTagTable title="Ground Truth" entities={truth} />
            </Grid>
          </Grid>
        </ExpansionPanelDetails>
      </ExpansionPanel>
    )
  }
}

const StyledEntry = withStyles(panelStyle)(Entry)

class Breakdown extends Component {

  constructor(props) {
    super(props)
    this.handleChange = this.handleChange.bind(this)
  }

  state = {
    expanded: null
  }

  handleChange = id => (event, expanded) => {
    this.setState({ expanded: expanded ? id : false })
  }

  render() {
    const { breakdownList, dp } = this.props
    const { expanded } = this.state
    return (
      <div style={{width: '100%'}}>
        {
          breakdownList.map(breakdown => 
            <StyledEntry breakdown={breakdown} handleChange={this.handleChange} expanded={expanded} dp={dp} />  
          )
        }
      </div>
    )
  }

}

class Scores extends Component {

  render() {
    const { result, ent_f1, attr_f1, dp } = this.props
    return (
      <Grid container spacing={24}>
        <Grid item lg={4}>
          <Paper style={{textAlign: 'center', padding: '10px', marginBottom: '40px'}}>
            <Typography color="textSecondary" gutterBottom>
              Average Combined F-Score
            </Typography>
            <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
              {Number(result).toFixed(dp)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item lg={4}>
          <Paper style={{textAlign: 'center', padding: '10px', marginBottom: '40px'}}>
            <Typography color="textSecondary" gutterBottom>
              Average Entity F-Score
            </Typography>
            <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
              {Number(ent_f1).toFixed(dp)}
            </Typography>
          </Paper>
        </Grid>
        <Grid item lg={4}>
          <Paper style={{textAlign: 'center', padding: '10px', marginBottom: '40px'}}>
            <Typography color="textSecondary" gutterBottom>
              Average Attribute F-Score
            </Typography>
            <Typography variant="h3" component="h2" style={{marginBottom: '20px'}}>
              {Number(attr_f1).toFixed(dp)}
            </Typography>
          </Paper>
        </Grid>
      </Grid>

    )
  }
}

class Evaluator extends Component {

  constructor(props) {
    super(props)
    this.dp = 3
  }

  state = {
    result: null,
    breakdown: null,
    loading: true,
  }

  componentWillMount() {
    axios.get('/test')
      .then(({ data }) => {
        console.log(data)
        const { result, ent_f1, attr_f1, breakdown } = data
        this.setState({ loading: false, result: result, ent_f1: ent_f1, attr_f1: attr_f1, breakdown: breakdown })
      })
  }

  render() {
    const dp = this.dp
    const { result, ent_f1, attr_f1, breakdown, loading } = this.state
    return (
      <>
      <Heading text="Model Evaluation" />
      {loading && <Loader />}
      {!loading && 
        <>
        <Scores result={result} ent_f1={ent_f1} attr_f1={attr_f1} dp={dp}/>
        <Breakdown breakdownList={breakdown} dp={dp}/>
        </>
      }
      </>
    )

  }

}

export default Evaluator