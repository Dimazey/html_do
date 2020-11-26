class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.output:
            with open(self.output, 'w') as f:
                f.write('<!DOCTYPE html>\n<html lang="en">\n')
                for child in self.children:
                    f.write(str(child))
                f.write('</html>')
        else:
            print('<!DOCTYPE html>'+'\n'+'<html lang="en">')
            for child in self.children:
                print(str(child))
            print('</html>')

    def __iadd__(self, other):
        self.children.append(other)
        return self


class TopLevelTag:
    def __init__(self, TopLevelTag):
        self.children = []
        self.TopLevelTag = TopLevelTag

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self


    def __str__(self):
        if  self.children:
            opening = '<%s>' % self.TopLevelTag
            internal = ''
            for child in self.children:
                internal += str(child)
            ending = '</%s>' % self.TopLevelTag
            return opening + '\n' + internal + ending + '\n'
        else:
            return "<{TopLevelTag}></{TopLevelTag}>".format(
                    TopLevelTag = self.TopLevelTag)

    def __iadd__(self, other):
        self.children.append(other)
        return self


class Tag(TopLevelTag):
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if  self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + '\n' + internal + '\n' + ending + '\n'
        else:
            if self.is_single:
                return "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)

            else:
                return "<{tag} {attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text)

if __name__ == "__main__":
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image='responsive') as img:
                    div += img

                body += div

            doc += body