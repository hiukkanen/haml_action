#!/usr/bin/env ruby
# This is used with apache actions_module.
# This is propably too slow for anything but was fun to make.
# How to configure your apache:
#  AddHandler cgi-script .cgi
#  Action render-haml /cgi-bin/haml_action.cgi
#  AddHandler render-haml .haml
# In cgi-bin directory:
#  SetHandler cgi-script
#  Options ExecCGI
# Also remember to a2enmod actions.
#
# This uses HAML::Engine (http://haml-lang.com/) to convert static haml files to html files with headers.
# It is possible to require another .haml files with "= h 'somefile.haml'".
# It is also possible to use layout for .haml file using "- layout 'somelayout.haml'".
# Layout should include line "= yield" where layout expects its content.
#
# Licensed under the MIT License.
require 'rubygems'
require 'haml'
require 'cgi'

module HamlAction

  # Returns rendered haml file. If haml file specifies layout
  # this will also wrap wanted layout around it.
  def HamlAction.render_haml filename
    template = File.read(filename)
    haml_engine = Haml::Engine.new(template)
    if block_given?
      output = haml_engine.render {yield}
    else
      output = haml_engine.render
    end
    if $layout
      temp_layout = $layout
      $layout = nil
      render_haml(absolute_name temp_layout) {output}
    else
      output
    end
  end

  # Can be used from .haml files to require another haml file.
  def h filename
    HamlAction::render_haml HamlAction::absolute_name filename
  end

  # Can be used from .haml file to specify layout in which
  # currently rendered .haml file belongs to.
  def layout filename
    $layout = filename
  end

  private

  # Returns ablsolute filename for relative used in
  # .haml files.
  def HamlAction.absolute_name filename
    source_file = ENV['PATH_TRANSLATED']
    filename = "#{File.dirname(source_file)}/#{filename}"
  end

end

# Includes h and layout to Haml Helpers
module Haml
  module Helpers
    include HamlAction
  end
end

# "Main method"
# Ouputs rendered .haml file(s) with html headers.
cgi = CGI.new
cgi.out {
  template = ENV['PATH_TRANSLATED']
  HamlAction::render_haml template
}
