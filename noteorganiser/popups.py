from PySide import QtGui

from constants import EXTENSION


class Dialog(QtGui.QDialog):
    """
    Model for dialogs in Note Organiser (pop-up windows)

    """
    def __init__(self, parent=None):
        """Define the shortcuts"""
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.info = parent.info
        self.log = parent.log

        # Define Ctrl+W to close it, and overwrite Esc
        _ = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+W'),
                            self, self.clean_accept)
        _ = QtGui.QShortcut(QtGui.QKeySequence('Esc'),
                            self, self.clean_reject)

    def clean_accept(self):
        """Logging the closing of the popup"""
        self.log.info("%s form suceeded!" % self.__class__.__name__)
        self.accept()

    def clean_reject(self):
        """Logging the rejection of the popup"""
        self.log.info("Aborting %s form" % self.__class__.__name__)
        self.reject()


class NewNotebook(Dialog):

    def __init__(self, parent=None):
        Dialog.__init__(self, parent)
        self.names = [elem.strip(EXTENSION) for elem in self.info.notebooks]
        self.initUI()

    def initUI(self):
        self.log.info("Creating a 'New Notebook' form")

        self.setWindowTitle("New notebook")

        # Define global vertical layout
        vboxLayout = QtGui.QVBoxLayout()

        # Define the fields:
        # Name (text field)
        # type (so far, standard)
        formLayout = QtGui.QFormLayout()
        self.nameLineEdit = QtGui.QLineEdit()
        # Query the type of notebook
        self.notebookType = QtGui.QComboBox()
        self.notebookType.addItem("Standard")

        formLayout.addRow(self.tr("Notebook's &name:"), self.nameLineEdit)
        formLayout.addRow(self.tr("&Notebook's &type:"), self.notebookType)
        vboxLayout.addLayout(formLayout)

        hboxLayout = QtGui.QHBoxLayout()

        # Add the "Create" button, as a confirmation, and the "Cancel" one
        create = QtGui.QPushButton("&Create")
        create.clicked.connect(self.create_notebook)
        cancel = QtGui.QPushButton("C&ancel")
        cancel.clicked.connect(self.clean_reject)
        hboxLayout.addWidget(create)
        hboxLayout.addWidget(cancel)
        vboxLayout.addLayout(hboxLayout)

        # Create a status bar
        self.statusBar = QtGui.QStatusBar()
        vboxLayout.addWidget(self.statusBar)

        self.setLayout(vboxLayout)

    def create_notebook(self):
        """Query the entry fields and append the notebook list"""
        desired_name = self.nameLineEdit.text()
        self.log.info("Desired Notebook name: "+desired_name)
        if not desired_name or len(desired_name) < 2:
            self.statusBar.showMessage("name too short", 2000)
            self.log.info("name rejected: too short")
        else:
            if desired_name in self.names:
                self.statusBar.showMessage("name already used", 2000)
                self.log.info("name rejected: already used")
            else:
                # Actually creating the notebook
                self.info.notebooks.append(desired_name)
                self.statusBar.showMessage("Creating notebook", 2000)
                self.accept()


class NewEntry(Dialog):

    def __init__(self, parent=None):
        Dialog.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.log.info("Creating a 'New Entry' form")

        self.setWindowTitle("New entry")

        # Define global vertical layout
        vboxLayout = QtGui.QVBoxLayout()

        # Define the main window horizontal layout
        hboxLayout = QtGui.QHBoxLayout()

        # Define the fields: Name, tags and body
        formLayout = QtGui.QFormLayout()
        self.titleLineEdit = QtGui.QLineEdit()
        self.tagsLineEdit = QtGui.QLineEdit()
        self.corpusBox = QtGui.QTextEdit()

        formLayout.addRow(self.tr("&Title:"), self.titleLineEdit)
        formLayout.addRow(self.tr("Ta&gs:"), self.tagsLineEdit)
        formLayout.addRow(self.tr("&Body:"), self.corpusBox)

        hboxLayout.addLayout(formLayout)

        # Define the RHS with Ok, Cancel and list of tags TODO)
        buttonLayout = QtGui.QVBoxLayout()

        okButton = QtGui.QPushButton("Ok")
        okButton.clicked.connect(self.creating_entry)
        acceptShortcut = QtGui.QShortcut(
            QtGui.QKeySequence(self.tr("Shift+Enter")), self.corpusBox)
        acceptShortcut.activated.connect(self.creating_entry)

        cancelButton = QtGui.QPushButton("&Cancel")
        cancelButton.clicked.connect(self.clean_reject)

        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        hboxLayout.addLayout(buttonLayout)
        # Create the status bar
        self.statusBar = QtGui.QStatusBar(self)
        # Create a permanent widget displaying what we are doing
        statusWidget = QtGui.QLabel("Creating new entry")
        self.statusBar.addPermanentWidget(statusWidget)

        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.statusBar)

        # Set the global layout
        self.setLayout(vboxLayout)

    def creating_entry(self):
        # Check if title is valid (non-empty)
        title = self.titleLineEdit.text()
        if not title or len(title) < 2:
            self.statusBar.showMessage(self.tr("Invalid title"), 2000)
            return
        tags = self.tagsLineEdit.text()
        if not tags or len(tags) < 2:
            self.statusBar.showMessage(self.tr("Invalid tags"), 2000)
            return
        tags = [tag.strip() for tag in tags.split(',')]
        corpus = self.corpusBox.toPlainText()
        if not corpus or len(corpus) < 2:
            self.statusBar.showMessage(self.tr("Empty entry"), 2000)
            return
        # Storing the variables to be recovered afterwards
        self.title = title
        self.tags = tags
        self.corpus = corpus
        self.clean_accept()
