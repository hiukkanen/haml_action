require 'test/unit'
load 'haml_action.cgi'

class TestHamlAction < Test::Unit::TestCase
  def test_should_fail_with_invalid_filename
    assert_raise Errno::ENOENT do
      HamlAction::render_haml "invalid"
    end
  end

  def test_should_get_correct_output_using_h_and_layout
    output = HamlAction::render_haml "./testfiles/h_and_layout.haml"
    expected = "<body>\n  <h1>\n    <p>hi</p>\n    <p>\n      Some paragraph text\n    </p>\n  </h1>\n</body>\n"
    assert_equal expected, output
  end

  def test_should_get_correct_output_using_dl_entry
    output = HamlAction::render_haml "./testfiles/dl_entry.haml"
    expected = "<dt>CoffeeScript</dt>\n<ds>CoffeeScript is a little language that compiles into JavaScript</ds>\n"
    assert_equal expected, output
  end

end
