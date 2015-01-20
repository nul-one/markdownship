
template='''<!DOCTYPE HTML>
<html>

  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style type="text/css">
      html {
        font-family: verdana, arial;
      }
      body {
        color             : #000;
        background-color  : #fff;
      }
  
      table {
        font-family: mono;
        font-size         : 80%;
        border-width      : 1px;
        border-color      : #666;
        border-collapse   : collapse;
      }
      table th {
        border-width      : 1px;
        padding           : 8px;
        border-style      : solid;
        border-color      : #666;
        background-color  : #eee;
      }
      table td {
        border-width      : 1px;
        padding           : 8px;
        border-style      : solid;
        border-color      : #666;
      }
  
      code {
        color             : #000;
        background-color  : #eee;
        padding           : 2px;
        margin            : 0px;
      }
      .codehilite {
        color             : #000;
        background-color  : #eee;
        border-style      : solid;
        border-width      : 1px;
        border-color      : #666;
        border-radius     : 5px;
        padding           : 6px;
        overflow          : auto;
      }
      .codehilite code {
        background-color  : #eee;
        padding           : 0px;
        margin            : 0px;
      }

      blockquote {
        padding-left      : 5px;
        border-color      : #aaa;
        border-style      : solid;
        border-width      : 0 0 0 5px;
      }
  
      #wrapper {
        /*width             : 700px;*/
        margin            : 0 auto;
        padding           : 0px;
      }
      #toc {
        background-color  : #fff;
        margin            : 10px 0 10px 0;
        padding           : 10px;
        border-style      : solid;
        border-width      : 1px;
        border-color      : #ddd;
        border-radius     : 3px;
        float             : left;
      }
      #contents {
        background-color  : #fff;
        margin            : 10px 0 10px 0;
        padding           : 10px;
        border-style      : solid;
        border-width      : 1px;
        border-color      : #ddd;
        border-radius     : 3px;
      }

      h1 {
        border-style      : solid;
        border-width      : 0 0 1px 0;
        border-color      : #aaa;
      }
  
      h2 {
        border-style      : solid;
        border-width      : 0 0 1px 0;
        border-color      : #ddd;
      }
  
      .hll { background-color: #ffffcc }
      .c { color: #999988; font-style: italic } /* Comment */
      .err { color: #a61717; background-color: #e3d2d2 } /* Error */
      .k { color: #000000; font-weight: bold } /* Keyword */
      .o { color: #000000; font-weight: bold } /* Operator */
      .cm { color: #999988; font-style: italic } /* Comment.Multiline */
      .cp { color: #999999; font-weight: bold; font-style: italic } /* Comment.Preproc */
      .c1 { color: #999988; font-style: italic } /* Comment.Single */
      .cs { color: #999999; font-weight: bold; font-style: italic } /* Comment.Special */
      .gd { color: #000000; background-color: #ffdddd } /* Generic.Deleted */
      .ge { color: #000000; font-style: italic } /* Generic.Emph */
      .gr { color: #aa0000 } /* Generic.Error */
      .gh { color: #999999 } /* Generic.Heading */
      .gi { color: #000000; background-color: #ddffdd } /* Generic.Inserted */
      .go { color: #888888 } /* Generic.Output */
      .gp { color: #555555 } /* Generic.Prompt */
      .gs { font-weight: bold } /* Generic.Strong */
      .gu { color: #aaaaaa } /* Generic.Subheading */
      .gt { color: #aa0000 } /* Generic.Traceback */
      .kc { color: #000000; font-weight: bold } /* Keyword.Constant */
      .kd { color: #000000; font-weight: bold } /* Keyword.Declaration */
      .kn { color: #000000; font-weight: bold } /* Keyword.Namespace */
      .kp { color: #000000; font-weight: bold } /* Keyword.Pseudo */
      .kr { color: #000000; font-weight: bold } /* Keyword.Reserved */
      .kt { color: #445588; font-weight: bold } /* Keyword.Type */
      .m { color: #009999 } /* Literal.Number */
      .s { color: #d01040 } /* Literal.String */
      .na { color: #008080 } /* Name.Attribute */
      .nb { color: #0086B3 } /* Name.Builtin */
      .nc { color: #445588; font-weight: bold } /* Name.Class */
      .no { color: #008080 } /* Name.Constant */
      .nd { color: #3c5d5d; font-weight: bold } /* Name.Decorator */
      .ni { color: #800080 } /* Name.Entity */
      .ne { color: #990000; font-weight: bold } /* Name.Exception */
      .nf { color: #990000; font-weight: bold } /* Name.Function */
      .nl { color: #990000; font-weight: bold } /* Name.Label */
      .nn { color: #555555 } /* Name.Namespace */
      .nt { color: #000080 } /* Name.Tag */
      .nv { color: #008080 } /* Name.Variable */
      .ow { color: #000000; font-weight: bold } /* Operator.Word */
      .w { color: #bbbbbb } /* Text.Whitespace */
      .mf { color: #009999 } /* Literal.Number.Float */
      .mh { color: #009999 } /* Literal.Number.Hex */
      .mi { color: #009999 } /* Literal.Number.Integer */
      .mo { color: #009999 } /* Literal.Number.Oct */
      .sb { color: #d01040 } /* Literal.String.Backtick */
      .sc { color: #d01040 } /* Literal.String.Char */
      .sd { color: #d01040 } /* Literal.String.Doc */
      .s2 { color: #d01040 } /* Literal.String.Double */
      .se { color: #d01040 } /* Literal.String.Escape */
      .sh { color: #d01040 } /* Literal.String.Heredoc */
      .si { color: #d01040 } /* Literal.String.Interpol */
      .sx { color: #d01040 } /* Literal.String.Other */
      .sr { color: #009926 } /* Literal.String.Regex */
      .s1 { color: #d01040 } /* Literal.String.Single */
      .ss { color: #990073 } /* Literal.String.Symbol */
      .bp { color: #999999 } /* Name.Builtin.Pseudo */
      .vc { color: #008080 } /* Name.Variable.Class */
      .vg { color: #008080 } /* Name.Variable.Global */
      .vi { color: #008080 } /* Name.Variable.Instance */
      .il { color: #009999 } /* Literal.Number.Integer.Long */

    </style>
  </head>

  <body>
    <div id='wrapper'>
      <div id='contents'>
        %markdown%
      </div>
    </div>
  </body>

</html>
'''